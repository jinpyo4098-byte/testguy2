import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(page_title="Gravity Arrow", layout="wide")

st.title("🏹 Gravity Arrow: Planet Environment & Arrow Mechanics")
st.markdown("과녁을 맞히면 화살이 즉시 리필되고, 빗나가면 화면 밖으로 사라진 후 **1초 뒤에 리필**됩니다. 상단의 행성 버튼을 눌러 배경과 중력을 변경해 보세요.")

# 게임 HTML/CSS/JS 전체 코드
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gravity Arrow</title>
    <style>
        body { margin: 0; padding: 0; overflow: hidden; background-color: #000; user-select: none; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        #gameCanvas { display: block; width: 100vw; height: 100vh; }
        #ui-layer { position: absolute; top: 0; left: 0; width: 100%; pointer-events: none; padding: 20px; box-sizing: border-box; }
        .hud-text { color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8); margin: 0; font-weight: bold; }
        #score-disp { font-size: 32px; color: #ffcc00; }
        #combo-wrapper { font-size: 24px; color: #ff3e3e; margin-top: 5px; transition: opacity 0.3s; }
        .hidden { opacity: 0; }
        
        #planet-controls { position: absolute; top: 20px; right: 20px; pointer-events: auto; display: flex; gap: 10px; }
        .btn-planet {
            padding: 10px 15px; border: 2px solid rgba(255,255,255,0.5); border-radius: 8px;
            background: rgba(0,0,0,0.6); color: white; font-weight: bold; cursor: pointer;
            transition: all 0.2s; text-transform: uppercase;
        }
        .btn-planet:hover { background: rgba(255,255,255,0.2); border-color: white; }
        .btn-planet.active { background: #3182ce; border-color: #63b3ed; }
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    
    <div id="ui-layer">
        <h1 class="hud-text">SCORE: <span id="score-disp">0</span></h1>
        <div id="combo-wrapper" class="hud-text hidden"><span id="combo-disp">0 COMBO</span></div>
    </div>

    <div id="planet-controls">
        <button class="btn-planet active" onclick="changePlanet('earth')" id="btn-earth">Earth</button>
        <button class="btn-planet" onclick="changePlanet('moon')" id="btn-moon">Moon</button>
        <button class="btn-planet" onclick="changePlanet('mars')" id="btn-mars">Mars</button>
        <button class="btn-planet" onclick="changePlanet('venus')" id="btn-venus">Venus</button>
        <button class="btn-planet" onclick="changePlanet('europa')" id="btn-europa">Europa</button>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        // 1. 행성 및 환경 데이터 설정
        const planets = {
            earth:  { g: 0.15, color: '#1E90FF', name: 'Earth' },
            moon:   { g: 0.05, color: '#A9A9A9', name: 'Moon' },
            mars:   { g: 0.1,  color: '#FFA500', name: 'Mars' },
            venus:  { g: 0.14, color: '#FFD700', name: 'Venus' },
            europa: { g: 0.08, color: '#E0FFFF', name: 'Europa' }
        };
        let currentPlanetKey = 'earth';
        let currentGravity = planets.earth.g;

        // 2. 게임 상태 및 오브젝트 변수
        let gameActive = true;
        let score = 0;
        let combo = 0;
        let maxCombo = 0;
        
        let isBuffed = false;
        let buffTimer = 0;
        let shakeIntensity = 0;

        let bowPos = { x: 150, y: canvas.height / 2 };
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let dragEnd = { x: 0, y: 0 };
        
        let activeArrows = [];
        let currentArrow = { isApple: false };
        let appleTrajectoryVisible = true;
        let appleTimer = 0;

        // [핵심] 화살 리필 시스템 변수
        let canShoot = true; 
        let arrowReloadTimer = 0; // 빗나갔을 때 60프레임(약 1초) 대기

        let target = {
            x: canvas.width - 200, y: canvas.height / 2,
            radiusD: 50, speed: 2, dir: 1, visible: true, respawnTimer: 0
        };

        let meteor = { active: false, x: 0, y: 0, vx: 0, vy: 0, radius: 25, destroyed: false };
        let particles = [];
        let scoreTexts = [];
        let weatherParticles = []; // 날씨/먼지 이펙트 배열

        // 날씨 파티클 초기화
        function initWeather() {
            weatherParticles = [];
            let count = 0;
            if(currentPlanetKey === 'earth') count = 15; // 구름
            if(currentPlanetKey === 'mars') count = 50;  // 먼지
            if(currentPlanetKey === 'venus') count = 100; // 짙은 먼지
            if(currentPlanetKey === 'europa') count = 150; // 눈

            for(let i=0; i<count; i++) {
                weatherParticles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    size: Math.random() * 3 + 1,
                    speedX: (Math.random() - 0.5) * 2,
                    speedY: Math.random() * 2 + 1
                });
            }
        }
        initWeather();

        // 3. UI 조작 함수
        window.changePlanet = function(key) {
            currentPlanetKey = key;
            currentGravity = planets[key].g;
            document.querySelectorAll('.btn-planet').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`btn-${key}`).classList.add('active');
            target.color = planets[key].color;
            initWeather();
        };

        // 4. 이펙트 생성 함수
        function createExplosion(x, y, color, count) {
            for(let i=0; i<count; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 10, vy: (Math.random() - 0.5) * 10,
                    radius: Math.random() * 4 + 2, color: color,
                    alpha: 1, decay: Math.random() * 0.02 + 0.01
                });
            }
        }

        function createScoreText(x, y, text, color) {
            scoreTexts.push({ x: x, y: y, text: text, color: color, alpha: 1, vy: -1.5 });
        }

        function activateAbilityBuff() {
            isBuffed = true;
            buffTimer = 300; // 5초 유지
            currentArrow.isApple = true;
        }

        function deactivateAbilityBuff() {
            isBuffed = false;
            currentArrow.isApple = false;
        }

        // 운석 소환 타이머 (15초)
        setTimeout(() => {
            meteor.active = true;
            meteor.x = canvas.width;
            meteor.y = 100;
            meteor.vx = -4;
            meteor.vy = 2;
        }, 15000);

        // 5. 입력 처리 (화살 장전 상태일 때만 드래그 가능)
        canvas.addEventListener('pointerdown', (e) => {
            if(!canShoot || !gameActive) return;
            isDragging = true;
            dragStart = { x: e.clientX, y: e.clientY };
            dragEnd = { x: e.clientX, y: e.clientY };
        });

        canvas.addEventListener('pointermove', (e) => {
            if(isDragging) {
                dragEnd = { x: e.clientX, y: e.clientY };
                bowPos.y = e.clientY; // 궁수 위치도 마우스 Y축 따라감
            }
        });

        canvas.addEventListener('pointerup', (e) => {
            if(!isDragging || !canShoot) return;
            isDragging = false;
            
            let vx = (dragStart.x - dragEnd.x) * 0.25;
            let vy = (dragStart.y - dragEnd.y) * 0.25;
            
            if(vx > 2) {
                activeArrows.push({
                    x: bowPos.x, y: bowPos.y,
                    vx: vx, vy: vy,
                    isApple: currentArrow.isApple, width: 95, handled: false
                });
                canShoot = false; // 발사 후 즉시 장전 불가 상태로 전환
            }
        });

        // 궁수 드로잉
        function drawArcherCharacter(angle) {
            ctx.save();
            ctx.translate(bowPos.x - 40, bowPos.y);
            // 몸통
            ctx.fillStyle = "#2d3748";
            ctx.beginPath(); ctx.arc(0, 0, 20, 0, Math.PI*2); ctx.fill();
            // 눈
            ctx.fillStyle = "white";
            ctx.beginPath(); ctx.arc(10, -5, 4, 0, Math.PI*2); ctx.fill();
            ctx.restore();
        }

        // 화살 드로잉
        function drawArrowIcon(x, y, angle, isApple, customWidth) {
            ctx.save();
            ctx.translate(x, y); ctx.rotate(angle);
            let width = customWidth || 95; 
            
            ctx.strokeStyle = isApple ? "#ff3333" : "#e2e8f0";
            ctx.lineWidth = isApple ? 5.5 : 4.5; 
            ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(width/2, 0); ctx.stroke();

            ctx.fillStyle = isApple ? "#ff0000" : "#cbd5e1";
            ctx.beginPath(); ctx.moveTo(width/2, 0); ctx.lineTo(width/2 - 15, -8); ctx.lineTo(width/2 - 15, 8); ctx.closePath(); ctx.fill();

            ctx.fillStyle = isApple ? "#ffcc00" : "#3182ce";
            ctx.beginPath(); ctx.moveTo(-width/2, 0); ctx.lineTo(-width/2 - 8, -10); ctx.lineTo(-width/2 + 5, -10); ctx.lineTo(-width/2 + 12, 0); ctx.lineTo(-width/2 + 5, 10); ctx.lineTo(-width/2 - 8, 10); ctx.closePath(); ctx.fill();
            ctx.restore();
        }

        // 🌍 행성별 맞춤 타겟 드로잉
        function drawPlanetTarget(x, y, radius) {
            ctx.save();
            ctx.translate(x, y);

            // 기본 행성 배경 원
            ctx.beginPath(); ctx.arc(0, 0, radius, 0, Math.PI * 2);
            
            if(currentPlanetKey === 'earth') {
                ctx.fillStyle = "#1E90FF"; ctx.fill();
                ctx.fillStyle = "#32CD32";
                ctx.beginPath(); ctx.arc(-10, -10, 15, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(15, 10, 20, 0, Math.PI*2); ctx.fill();
            } 
            else if(currentPlanetKey === 'moon') {
                ctx.fillStyle = "#A9A9A9"; ctx.fill();
                ctx.fillStyle = "#4a4a4a"; // 검은/짙은 회색 자국
                ctx.beginPath(); ctx.arc(-15, -15, 8, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(10, -5, 5, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(-5, 20, 12, 0, Math.PI*2); ctx.fill();
            }
            else if(currentPlanetKey === 'mars') {
                ctx.fillStyle = "#FFA500"; ctx.fill();
                ctx.fillStyle = "#8B4513"; // 갈색 반점
                ctx.beginPath(); ctx.ellipse(0, 0, 30, 15, Math.PI/4, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.arc(-20, 15, 10, 0, Math.PI*2); ctx.fill();
            }
            else if(currentPlanetKey === 'venus') {
                ctx.fillStyle = "#FFD700"; ctx.fill();
                ctx.fillStyle = "#DAA520"; // 진노란색 반점
                ctx.beginPath(); ctx.ellipse(-10, 0, 40, 10, -Math.PI/6, 0, Math.PI*2); ctx.fill();
                ctx.beginPath(); ctx.ellipse(15, 15, 20, 8, Math.PI/3, 0, Math.PI*2); ctx.fill();
            }
            else if(currentPlanetKey === 'europa') {
                ctx.fillStyle = "#E0FFFF"; ctx.fill();
                ctx.strokeStyle = "#87CEFA"; // 빙판 금
                ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(-30, -20); ctx.lineTo(10, 0); ctx.lineTo(30, -10); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(-20, 30); ctx.lineTo(0, 10); ctx.lineTo(20, 20); ctx.stroke();
            }

            // 테두리
            ctx.strokeStyle = "rgba(255,255,255,0.5)"; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.arc(0, 0, radius, 0, Math.PI*2); ctx.stroke();
            
            ctx.restore();
        }

        // 🌌 행성별 배경 및 날씨 렌더링
        function drawEnvironment() {
            let skyColor, groundColor;
            
            if(currentPlanetKey === 'earth') {
                skyColor = '#87CEEB'; groundColor = '#8B4513';
            } else if(currentPlanetKey === 'moon') {
                skyColor = '#000000'; groundColor = '#555555';
            } else if(currentPlanetKey === 'mars') {
                skyColor = '#D2B48C'; groundColor = '#A0522D';
            } else if(currentPlanetKey === 'venus') {
                skyColor = '#BDB76B'; groundColor = '#DAA520';
            } else if(currentPlanetKey === 'europa') {
                skyColor = '#B0E0E6'; groundColor = '#E0FFFF';
            }

            // 하늘 렌더링
            ctx.fillStyle = skyColor;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 날씨/먼지 렌더링
            ctx.fillStyle = (currentPlanetKey === 'venus') ? '#DAA520' : 'white';
            if(currentPlanetKey === 'mars') ctx.fillStyle = '#8B4513';

            weatherParticles.forEach(p => {
                ctx.beginPath();
                if(currentPlanetKey === 'earth') {
                    // 구름
                    ctx.arc(p.x, p.y, p.size * 5, 0, Math.PI*2); ctx.fill();
                    p.x += 0.5;
                    if(p.x > canvas.width + 50) p.x = -50;
                } 
                else if(currentPlanetKey === 'venus') {
                    // 진노란색 먼지 (오른쪽에서 왼쪽)
                    ctx.fillRect(p.x, p.y, p.size * 4, 2);
                    p.x -= (p.speedX + 3);
                    if(p.x < -10) p.x = canvas.width + 10;
                }
                else if(currentPlanetKey === 'europa') {
                    // 눈 (위에서 아래)
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI*2); ctx.fill();
                    p.y += p.speedY;
                    if(p.y > canvas.height) p.y = -10;
                }
                else if(currentPlanetKey === 'mars') {
                    // 떠다니는 먼지
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI*2); ctx.fill();
                    p.x += p.speedX * 0.5; p.y += p.speedY * 0.2;
                    if(p.x > canvas.width) p.x = 0;
                    if(p.y > canvas.height) p.y = 0;
                }
            });

            // 바닥(Ground) 렌더링
            ctx.fillStyle = groundColor;
            if(currentPlanetKey === 'moon') {
                // 울퉁불퉁한 달 표면
                ctx.beginPath();
                ctx.moveTo(0, canvas.height);
                ctx.lineTo(0, canvas.height - 100);
                for(let i=0; i<=canvas.width; i+=100) {
                    ctx.quadraticCurveTo(i+50, canvas.height-130, i+100, canvas.height-100);
                }
                ctx.lineTo(canvas.width, canvas.height);
                ctx.fill();
            } 
            else if (currentPlanetKey === 'europa') {
                ctx.fillRect(0, canvas.height - 100, canvas.width, 100);
                // 얼음 갈라짐 묘사
                ctx.strokeStyle = '#87CEFA'; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(100, canvas.height - 50); ctx.lineTo(150, canvas.height - 80); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(500, canvas.height - 20); ctx.lineTo(550, canvas.height - 90); ctx.stroke();
            }
            else {
                ctx.fillRect(0, canvas.height - 100, canvas.width, 100);
            }
        }

        // 6. 메인 업데이트 루프
        function update() {
            // 능력치 유지시간 차감 연산
            if (gameActive && isBuffed) {
                buffTimer--;
                if(buffTimer <= 0) deactivateAbilityBuff();
            }

            if (gameActive) {
                // 과녁 움직임 및 리스폰
                if(target.visible) {
                    target.y += target.speed * target.dir;
                    if(target.y - target.radiusD < 140 || target.y + target.radiusD > canvas.height - 140) {
                        target.dir *= -1; 
                    }
                } else {
                    target.respawnTimer--;
                    if(target.respawnTimer <= 0) {
                        target.y = 180 + Math.random() * (canvas.height - 350);
                        target.visible = true;
                    }
                }

                // 화살 빗나감 리필 타이머 연산 (1초 대기)
                if (!canShoot && activeArrows.length === 0 && arrowReloadTimer > 0) {
                    arrowReloadTimer--;
                    if(arrowReloadTimer <= 0) {
                        canShoot = true; // 1초 뒤 화살 리필 완료
                    }
                }

                // 운석 이동 연산
                if(meteor.active) {
                    meteor.x += meteor.vx;
                    meteor.y += meteor.vy;
                    if(meteor.x < bowPos.x - 20) {
                        meteor.active = false;
                        createExplosion(meteor.x, meteor.y, "#94a3b8", 30);
                        shakeIntensity = 10;
                    }
                }
            }

            ctx.save();
            
            // 화면 흔들림 연출
            if (shakeIntensity > 0) {
                ctx.translate((Math.random() - 0.5) * shakeIntensity, (Math.random() - 0.5) * shakeIntensity);
                shakeIntensity *= 0.85; 
                if (shakeIntensity < 0.2) shakeIntensity = 0;
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // [요청 반영] 행성별 배경 및 날씨 그리기
            drawEnvironment();

            // 버프 모드 붉은 화면 연출
            if(isBuffed && gameActive) {
                ctx.fillStyle = "rgba(255, 62, 62, 0.1)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            // 운석 렌더링
            if(meteor.active) {
                ctx.save();
                ctx.fillStyle = "rgba(239, 68, 68, 0.25)";
                ctx.beginPath(); ctx.arc(meteor.x, meteor.y, meteor.radius + 12 + Math.random()*6, 0, Math.PI*2); ctx.fill();
                let grad = ctx.createRadialGradient(meteor.x - 10, meteor.y - 10, 5, meteor.x, meteor.y, meteor.radius);
                grad.addColorStop(0, '#ff9e00'); grad.addColorStop(0.6, '#d946ef'); grad.addColorStop(1, '#450a0a');
                ctx.fillStyle = grad;
                ctx.beginPath(); ctx.arc(meteor.x, meteor.y, meteor.radius, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#ff0055"; ctx.lineWidth = 3; ctx.stroke();
                ctx.restore();
            }

            // [요청 반영] 🌍 행성 묘사 과녁 렌더링
            if(target.visible) {
                drawPlanetTarget(target.x, target.y, target.radiusD);
            }

            // 궁수 및 활시위 렌더링
            let dragAngle = Math.atan2(dragStart.y - dragEnd.y, dragStart.x - dragEnd.x);
            drawArcherCharacter(dragAngle);

            ctx.save();
            ctx.strokeStyle = isBuffed ? "#ff0055" : "#00d2ff";
            ctx.lineWidth = 5; 
            ctx.beginPath();
            ctx.arc(bowPos.x - 12, bowPos.y, 48, -Math.PI/2, Math.PI/2); 
            ctx.stroke();
            
            ctx.strokeStyle = "rgba(255,255,255,0.5)";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(bowPos.x - 12, bowPos.y - 48);
            if(isDragging) ctx.lineTo(dragEnd.x, dragEnd.y);
            else ctx.lineTo(bowPos.x - 12, bowPos.y);
            ctx.lineTo(bowPos.x - 12, bowPos.y + 48);
            ctx.stroke();
            ctx.restore();

            // [핵심 기믹] 장전 상태(canShoot)일 때만 활 시위에 화살 표시
            if(!isDragging && gameActive && canShoot) {
                drawArrowIcon(bowPos.x, bowPos.y, 0, currentArrow.isApple);
            }

            // 궤적 가이드라인 렌더링
            if (isDragging && appleTrajectoryVisible && gameActive && canShoot) {
                let tVx = (dragStart.x - dragEnd.x) * 0.25;
                if (tVx > 0) { 
                    ctx.save();
                    ctx.strokeStyle = currentArrow.isApple ? "#af0404" : "rgba(255, 255, 255, 0.7)";
                    ctx.lineWidth = 2.5; ctx.setLineDash([5, 5]);
                    ctx.beginPath();

                    let tX = bowPos.x; let tY = bowPos.y;
                    let tVy = (dragStart.y - dragEnd.y) * 0.25;

                    ctx.moveTo(tX, tY);
                    for (let i = 0; i < 60; i++) {
                        tX += tVx; tY += tVy; tVy += currentGravity; 
                        ctx.lineTo(tX, tY);
                        if(tX > canvas.width || tY > canvas.height || tY < 0) break;
                    }
                    ctx.stroke(); ctx.restore();
                    drawArrowIcon(dragEnd.x, dragEnd.y, dragAngle, currentArrow.isApple);
                }
            }

            // 화살 비행 및 충돌 처리
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                arrow.x += arrow.vx;
                arrow.y += arrow.vy;
                arrow.vy += currentGravity; // 행성별 중력 적용

                let arrowAngle = Math.atan2(arrow.vy, arrow.vx);
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.isApple, arrow.width);

                let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);

                // [화살 리필 로직 1] 화면 밖으로 빗나갔을 때 -> 1초 뒤 장전
                if (arrow.x > canvas.width + 50 || arrow.y > canvas.height + 50 || arrow.y < -50) {
                    if(!arrow.handled) {
                        combo = 0; document.getElementById('combo-wrapper').classList.add('hidden');
                        arrowReloadTimer = 60; // 60프레임(약 1초) 쿨타임 설정
                    }
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 특수 운석 충돌
                if(meteor.active) {
                    let distToMeteor = Math.hypot(arrowTipX - meteor.x, arrowTipY - meteor.y);
                    if(distToMeteor <= meteor.radius + 10) {
                        meteor.active = false;
                        activeArrows.splice(i, 1); 
                        createExplosion(meteor.x, meteor.y, "#ffcc00", 40);
                        createScoreText(meteor.x, meteor.y, "AWAKENING!!", "#ffcc00");
                        activateAbilityBuff();
                        canShoot = true; // 적중 시 즉시 리필
                        continue;
                    }
                }

                // [화살 리필 로직 2] 과녁 적중 시 -> 타겟 소멸 및 화살 즉시 리필
                if (target.visible && arrowTipX >= target.x - target.radiusD && arrowTipX <= target.x + target.radiusD && arrow.vx > 0) {
                    let dy = Math.abs(arrowTipY - target.y);

                    if (dy <= target.radiusD) {
                        arrow.handled = true;
                        
                        target.visible = false;
                        target.respawnTimer = 45; 

                        combo++;
                        if(combo > maxCombo) maxCombo = combo;
                        document.getElementById('combo-disp').innerText = `${combo} COMBO`;
                        document.getElementById('combo-wrapper').classList.remove('hidden');

                        let earnedPoints = 10 + Math.floor(combo / 3);
                        if(arrow.isApple) earnedPoints *= 2;
                        
                        score += earnedPoints;
                        document.getElementById('score-disp').innerText = score;

                        createScoreText(arrowTipX - 25, arrowTipY - 15, `+${earnedPoints}`, "#fff");
                        shakeIntensity = 7; 
                        createExplosion(arrowTipX, arrowTipY, "#fff", 20);

                        activeArrows.splice(i, 1); 
                        
                        canShoot = true; // 적중 시 쿨타임 없이 즉시 리필
                        arrowReloadTimer = 0; 
                        continue;
                    }
                }
            }

            // 파티클 엔진
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy; p.alpha -= p.decay;
                if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = p.alpha; ctx.fillStyle = p.color;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI*2); ctx.fill(); ctx.restore();
            }

            // 스코어 텍스트
            for (let i = scoreTexts.length - 1; i >= 0; i--) {
                let stx = scoreTexts[i];
                stx.y += stx.vy; stx.alpha -= 0.015;
                if(stx.alpha <= 0) { scoreTexts.splice(i, 1); continue; }
                ctx.save(); ctx.globalAlpha = stx.alpha; ctx.fillStyle = stx.color;
                ctx.font = "bold 26px 'Segoe UI'"; ctx.shadowColor = "rgba(0,0,0,0.5)"; ctx.shadowBlur = 4;
                ctx.fillText(stx.text, stx.x, stx.y); ctx.restore();
            }

            ctx.restore(); 
            requestAnimationFrame(update);
        }

        // 게임 루프 시작
        update();
    </script>
</body>
</html>
"""

components.html(game_html, height=850, scrolling=False)
