import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정 (16:9 비율을 위해 wide 모드 사용)
st.set_page_config(layout="wide", page_title="Gravity Arrow", page_icon="🏹")

# HTML, CSS, JavaScript를 포함한 전체 웹 게임 코드
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Gravity Arrow</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Malgun Gothic', sans-serif;
            color: white;
            user-select: none;
        }
        #game-container {
            position: relative;
            width: 1280px;
            height: 720px;
            box-shadow: 0 0 20px rgba(255,255,255,0.2);
            overflow: hidden;
        }
        canvas {
            display: block;
            width: 100%;
            height: 100%;
        }
        /* 화면 흔들림 애니메이션 */
        @keyframes shake {
            0% { transform: translate(1px, 1px) rotate(0deg); }
            10% { transform: translate(-1px, -2px) rotate(-1deg); }
            20% { transform: translate(-3px, 0px) rotate(1deg); }
            30% { transform: translate(3px, 2px) rotate(0deg); }
            40% { transform: translate(1px, -1px) rotate(1deg); }
            50% { transform: translate(-1px, 2px) rotate(-1deg); }
            60% { transform: translate(-3px, 1px) rotate(0deg); }
            70% { transform: translate(3px, 1px) rotate(-1deg); }
            80% { transform: translate(-1px, -1px) rotate(1deg); }
            90% { transform: translate(1px, 2px) rotate(0deg); }
            100% { transform: translate(1px, -2px) rotate(-1deg); }
        }
        .shake {
            animation: shake 0.5s;
            animation-iteration-count: 1;
        }
        /* UI 오버레이 */
        #ui-layer {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; /* 클릭은 캔버스로 통과 */
        }
        .hud-text {
            position: absolute;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 2px 2px 4px #000;
        }
        #score-board { top: 20px; right: 20px; text-align: right; }
        #combo-text { top: 80px; right: 20px; color: #FFD700; font-size: 36px; transition: transform 0.1s; }
        #info-board { top: 20px; left: 20px; }
        
        /* 메인 메뉴 */
        #main-menu {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            pointer-events: auto;
            z-index: 10;
        }
        h1 { font-size: 80px; margin-bottom: 10px; color: #00e5ff; text-shadow: 0 0 20px #00e5ff; }
        .planet-btn-group { display: flex; gap: 15px; margin: 30px 0; }
        .planet-btn {
            background: #222; border: 2px solid #555; color: white; padding: 15px 25px;
            font-size: 18px; border-radius: 30px; cursor: pointer; transition: 0.3s;
        }
        .planet-btn.active { border-color: #00e5ff; background: #005f73; }
        .planet-btn:hover { background: #444; }
        #start-btn {
            background: #007bff; border: none; color: white; padding: 20px 60px;
            font-size: 30px; border-radius: 50px; cursor: pointer;
            box-shadow: 0 0 15px #007bff; transition: 0.2s;
        }
        #start-btn:hover { transform: scale(1.05); }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="1280" height="720"></canvas>
    
    <div id="ui-layer">
        <div id="info-board" class="hud-text">
            남은 시간: <span id="time-left">15</span>초<br>
            중력 (<span id="planet-name">지구</span>): <span id="gravity-val">9.8</span> m/s²
        </div>
        <div id="score-board" class="hud-text">
            최고 기록: <span id="best-score">0</span>점<br>
            현재 점수: <span id="current-score">0</span>점
        </div>
        <div id="combo-text" class="hud-text" style="display:none;">COMBO x<span id="combo-val">0</span>!</div>
    </div>

    <div id="main-menu">
        <h1>Gravity Arrow</h1>
        <p style="font-size: 20px; color: #ccc;">활을 드래그하여 과녁을 맞추세요! (15초 제한)</p>
        <div class="planet-btn-group">
            <button class="planet-btn active" onclick="setPlanet('earth')">지구</button>
            <button class="planet-btn" onclick="setPlanet('moon')">달</button>
            <button class="planet-btn" onclick="setPlanet('mars')">화성</button>
            <button class="planet-btn" onclick="setPlanet('venus')">금성</button>
            <button class="planet-btn" onclick="setPlanet('europa')">유로파</button>
        </div>
        <button id="start-btn" onclick="startGame()">게임 시작</button>
    </div>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const container = document.getElementById('game-container');

    // 게임 상태 변수
    let isPlaying = false;
    let score = 0;
    let bestScore = 0;
    let timeLeft = 15;
    let combo = 0;
    let timerInterval;

    // 행성 데이터 (중력값 및 배경 입자색)
    const planets = {
        earth: { name: "지구", gravity: 9.8, bg: "#87CEEB", particle: "white", pType: "cloud" },
        moon: { name: "달", gravity: 1.6, bg: "#0f0f1a", particle: "#888", pType: "star" },
        mars: { name: "화성", gravity: 3.7, bg: "#8B4513", particle: "#CD5C5C", pType: "dust" },
        venus: { name: "금성", gravity: 8.9, bg: "#DAA520", particle: "#F0E68C", pType: "gas" },
        europa: { name: "유로파", gravity: 1.3, bg: "#E0FFFF", particle: "#fff", pType: "snow" }
    };
    let currentPlanet = 'earth';

    // 물리 및 렌더링 스케일 설정
    const scale = 5; // 중력 스케일 보정
    const baseArrowSpeed = 5; // 화살 기본 속도 계수

    // 활과 화살
    let bow = { x: 150, y: 550, isDragging: false, dragStart: {x:0, y:0}, dragCurrent: {x:0, y:0} };
    let arrows = [];
    let isGoldenReady = false;
    let goldenChangeTimer = 0;

    // 과녁
    let target = { 
        x: 1100, y: 360, radius: 80, dy: 2, 
        directionTimer: 0, isBroken: false, respawnTimer: 0 
    };

    // 파티클 (배경 및 이펙트)
    let bgParticles = [];
    let hitParticles = [];

    // 입력 처리
    canvas.addEventListener('mousedown', (e) => {
        if(!isPlaying) return;
        const rect = canvas.getBoundingClientRect();
        const mx = (e.clientX - rect.left) * (canvas.width / rect.width);
        const my = (e.clientY - rect.top) * (canvas.height / rect.height);
        
        // 활 근처 클릭 시 드래그 시작
        if(Math.hypot(mx - bow.x, my - bow.y) < 100) {
            bow.isDragging = true;
            bow.dragStart = {x: mx, y: my};
            bow.dragCurrent = {x: mx, y: my};
        }
    });

    canvas.addEventListener('mousemove', (e) => {
        if(bow.isDragging) {
            const rect = canvas.getBoundingClientRect();
            bow.dragCurrent.x = (e.clientX - rect.left) * (canvas.width / rect.width);
            bow.dragCurrent.y = (e.clientY - rect.top) * (canvas.height / rect.height);
        }
    });

    canvas.addEventListener('mouseup', (e) => {
        if(bow.isDragging && isPlaying) {
            bow.isDragging = false;
            shootArrow();
            prepareNextArrow();
        }
    });

    // 행성 선택
    window.setPlanet = function(planetKey) {
        currentPlanet = planetKey;
        document.querySelectorAll('.planet-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
        initBgParticles();
    };

    // 게임 시작
    window.startGame = function() {
        document.getElementById('main-menu').style.display = 'none';
        isPlaying = true;
        score = 0;
        timeLeft = 15;
        combo = 0;
        arrows = [];
        target.isBroken = false;
        updateUI();
        prepareNextArrow();
        
        timerInterval = setInterval(() => {
            timeLeft--;
            updateUI();
            if(timeLeft <= 0) endGame();
        }, 1000);
    };

    function endGame() {
        isPlaying = false;
        clearInterval(timerInterval);
        if(score > bestScore) bestScore = score;
        document.getElementById('main-menu').style.display = 'flex';
        document.getElementById('start-btn').innerText = "다시 시작";
    }

    function updateUI() {
        document.getElementById('time-left').innerText = timeLeft;
        document.getElementById('planet-name').innerText = planets[currentPlanet].name;
        document.getElementById('gravity-val').innerText = planets[currentPlanet].gravity.toFixed(1);
        document.getElementById('current-score').innerText = score;
        document.getElementById('best-score').innerText = bestScore;
    }

    function prepareNextArrow() {
        // 1/20 확률로 사과(골든) 화살
        isGoldenReady = Math.random() < 0.05;
    }

    function shootArrow() {
        let dx = bow.dragStart.x - bow.dragCurrent.x;
        let dy = bow.dragStart.y - bow.dragCurrent.y;
        
        // 힘 제한
        let power = Math.min(Math.hypot(dx, dy), 200) / 10; 
        let angle = Math.atan2(dy, dx);
        
        arrows.push({
            x: bow.x, y: bow.y,
            vx: Math.cos(angle) * power * baseArrowSpeed,
            vy: Math.sin(angle) * power * baseArrowSpeed,
            angle: angle,
            isGolden: isGoldenReady,
            trail: []
        });
    }

    // 과녁 파괴 및 화면 흔들림
    function breakTarget() {
        target.isBroken = true;
        target.respawnTimer = 60; // 1초 (60프레임)
        
        // 화면 흔들림 CSS 클래스 트리거
        container.classList.remove('shake');
        void container.offsetWidth; // 리플로우 강제
        container.classList.add('shake');

        // 파편 파티클 생성
        for(let i=0; i<30; i++) {
            hitParticles.push({
                x: target.x, y: target.y,
                vx: (Math.random() - 0.5) * 15,
                vy: (Math.random() - 0.5) * 15,
                life: 30,
                color: ['#ff0000', '#ffff00', '#ffffff'][Math.floor(Math.random()*3)]
            });
        }
    }

    // 콤보 텍스트 애니메이션
    function showCombo() {
        const cText = document.getElementById('combo-text');
        document.getElementById('combo-val').innerText = combo;
        cText.style.display = 'block';
        cText.style.transform = `scale(${1 + combo * 0.1})`;
        setTimeout(() => cText.style.transform = 'scale(1)', 100);
    }

    // 배경 파티클 초기화
    function initBgParticles() {
        bgParticles = [];
        for(let i=0; i<100; i++) {
            bgParticles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                size: Math.random() * 3 + 1,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2
            });
        }
    }

    // === 루프 및 렌더링 ===
    function gameLoop() {
        update();
        draw();
        requestAnimationFrame(gameLoop);
    }

    function update() {
        if(!isPlaying) return;

        let g = planets[currentPlanet].gravity / scale;

        // 골든 화살 궤적 변환 타이머
        goldenChangeTimer++;

        // 과녁 이동
        if(!target.isBroken) {
            target.y += target.dy;
            target.directionTimer++;
            if(target.directionTimer > 300) { // 약 5초 (60fps 기준)
                target.dy *= -1;
                target.directionTimer = 0;
            }
            if(target.y < 100 || target.y > canvas.height - 100) target.dy *= -1;
        } else {
            target.respawnTimer--;
            if(target.respawnTimer <= 0) {
                target.isBroken = false;
                target.y = Math.random() * 400 + 150; // 랜덤 높이 리스폰
            }
        }

        // 화살 물리 업데이트
        for(let i = arrows.length - 1; i >= 0; i--) {
            let a = arrows[i];
            
            // 골든 화살 불규칙 운동
            if(a.isGolden && goldenChangeTimer % 60 === 0) {
                a.vy += (Math.random() - 0.5) * 5;
            }

            a.vy += g; // 중력 적용
            a.x += a.vx;
            a.y += a.vy;
            a.angle = Math.atan2(a.vy, a.vx); // 비행 방향으로 각도 회전
            
            a.trail.push({x: a.x, y: a.y});
            if(a.trail.length > 10) a.trail.shift(); // 잔상 길이 조절

            // 충돌 감지 (A, B, C, D 구역)
            if(!target.isBroken) {
                let dist = Math.hypot(a.x - target.x, a.y - target.y);
                if(dist < target.radius) {
                    let pts = 0;
                    if(dist < target.radius * 0.25) pts = 10;      // A
                    else if(dist < target.radius * 0.5) pts = 5; // B
                    else if(dist < target.radius * 0.75) pts = 2;// C
                    else pts = 1;                                // D
                    
                    if(a.isGolden) pts *= 2; // 골든 2배

                    score += pts;
                    combo++;
                    showCombo();
                    updateUI();
                    breakTarget();
                    arrows.splice(i, 1);
                    continue;
                }
            }

            // 화면 밖으로 나가면 삭제
            if(a.x > canvas.width + 100 || a.y > canvas.height + 100) {
                arrows.splice(i, 1);
                combo = 0; // 콤보 초기화
                document.getElementById('combo-text').style.display = 'none';
            }
        }

        // 배경 파티클 업데이트
        bgParticles.forEach(p => {
            if(planets[currentPlanet].pType === "gas") { p.vx += 0.1; p.x += p.vx; p.y += (Math.random()-0.5); } // 금성 강풍
            else { p.x += p.vx; p.y += p.vy; }
            
            if(p.x < 0) p.x = canvas.width;
            if(p.x > canvas.width) p.x = 0;
            if(p.y < 0) p.y = canvas.height;
            if(p.y > canvas.height) p.y = 0;
        });

        // 타격 파티클 업데이트
        for(let i = hitParticles.length - 1; i >= 0; i--) {
            hitParticles[i].x += hitParticles[i].vx;
            hitParticles[i].y += hitParticles[i].vy;
            hitParticles[i].life--;
            if(hitParticles[i].life <= 0) hitParticles.splice(i, 1);
        }
    }

    function draw() {
        // 배경 그리기 (행성 테마)
        ctx.fillStyle = planets[currentPlanet].bg;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // 지표면 (어두운 실루엣)
        ctx.fillStyle = "#111";
        ctx.beginPath();
        ctx.moveTo(0, canvas.height - 50);
        ctx.quadraticCurveTo(canvas.width/2, canvas.height - 100, canvas.width, canvas.height - 40);
        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.fill();

        // 배경 파티클
        ctx.fillStyle = planets[currentPlanet].particle;
        bgParticles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
            ctx.fill();
        });

        // 궤적 점선 예측 (드래그 중)
        if(bow.isDragging) {
            let dx = bow.dragStart.x - bow.dragCurrent.x;
            let dy = bow.dragStart.y - bow.dragCurrent.y;
            let power = Math.min(Math.hypot(dx, dy), 200) / 10; 
            let angle = Math.atan2(dy, dx);
            
            let g = planets[currentPlanet].gravity / scale;
            let tx = bow.x;
            let ty = bow.y;
            let tvx = Math.cos(angle) * power * baseArrowSpeed;
            let tvy = Math.sin(angle) * power * baseArrowSpeed;

            ctx.fillStyle = "rgba(255, 255, 255, 0.5)";
            for(let i=0; i<30; i++) {
                tx += tvx;
                tvy += g;
                ty += tvy;
                if(i % 3 === 0) { // 점선 효과
                    ctx.beginPath();
                    ctx.arc(tx, ty, 3, 0, Math.PI*2);
                    ctx.fill();
                }
            }
        }

        // 과녁 그리기
        if(!target.isBroken) {
            const colors = ["#fff", "#000", "#00aaff", "#ff0000"]; // D, C, B, A
            for(let i=3; i>=0; i--) {
                ctx.fillStyle = colors[i];
                ctx.beginPath();
                ctx.arc(target.x, target.y, target.radius * ((i+1)*0.25), 0, Math.PI*2);
                ctx.fill();
                ctx.lineWidth = 2;
                ctx.strokeStyle = "#222";
                ctx.stroke();
            }
        }

        // 타격 파편 그리기
        hitParticles.forEach(p => {
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, 4, 0, Math.PI*2);
            ctx.fill();
        });

        // 활 그리기 (단순화된 활 모양)
        ctx.save();
        ctx.translate(bow.x, bow.y);
        if(bow.isDragging) {
            let dx = bow.dragStart.x - bow.dragCurrent.x;
            let dy = bow.dragStart.y - bow.dragCurrent.y;
            ctx.rotate(Math.atan2(dy, dx));
        }
        ctx.strokeStyle = "#8B4513"; // 나무색
        ctx.lineWidth = 5;
        ctx.beginPath();
        ctx.arc(0, 0, 50, -Math.PI/2.5, Math.PI/2.5);
        ctx.stroke();
        // 활 시위
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(35, -35);
        if(bow.isDragging) ctx.lineTo(-Math.min(Math.hypot(bow.dragStart.x - bow.dragCurrent.x, bow.dragStart.y - bow.dragCurrent.y)/3, 40), 0);
        else ctx.lineTo(10, 0);
        ctx.lineTo(35, 35);
        ctx.stroke();
        ctx.restore();

        // 발사 대기 중인 화살 그리기
        if(!bow.isDragging && !isPlaying) return; // 메뉴창에선 대기 화살 안그림
        if(!bow.isDragging) {
            drawArrowShape(bow.x + 20, bow.y, 0, isGoldenReady);
        } else {
            let dx = bow.dragStart.x - bow.dragCurrent.x;
            let dy = bow.dragStart.y - bow.dragCurrent.y;
            let angle = Math.atan2(dy, dx);
            let pull = Math.min(Math.hypot(dx, dy)/3, 40);
            drawArrowShape(bow.x - pull, bow.y, angle, isGoldenReady);
        }

        // 날아가는 화살 그리기
        arrows.forEach(a => {
            // 잔상 효과 (모션 블러)
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            if(a.trail.length > 0) {
                ctx.lineTo(a.trail[0].x, a.trail[0].y);
                ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
                ctx.lineWidth = 3;
                ctx.stroke();
            }
            drawArrowShape(a.x, a.y, a.angle, a.isGolden);
        });
    }

    // 디테일한 화살 그리기 함수
    function drawArrowShape(x, y, angle, isGolden) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(angle);
        
        // 화살대 (카본/나무 느낌)
        ctx.fillStyle = isGolden ? "#FFD700" : "#3e2723";
        ctx.fillRect(-40, -1.5, 80, 3);
        
        // 화살촉 (강철/티타늄)
        ctx.fillStyle = "#cfd8dc";
        ctx.beginPath();
        ctx.moveTo(40, -3);
        ctx.lineTo(50, 0);
        ctx.lineTo(40, 3);
        ctx.fill();
        
        // 화살 깃 (3개지만 2D 단면이므로 2개 표현)
        ctx.fillStyle = isGolden ? "#ff5252" : "#ffffff";
        ctx.beginPath();
        ctx.moveTo(-35, -1.5);
        ctx.lineTo(-45, -8);
        ctx.lineTo(-40, -1.5);
        ctx.fill();
        ctx.beginPath();
        ctx.moveTo(-35, 1.5);
        ctx.lineTo(-45, 8);
        ctx.lineTo(-40, 1.5);
        ctx.fill();

        // 꼬리 홈 (Nock)
        ctx.fillStyle = "#000";
        ctx.fillRect(-42, -2, 2, 4);

        if(isGolden) {
            // 사과 꽂힌 표현
            ctx.fillStyle = "red";
            ctx.beginPath();
            ctx.arc(35, 0, 6, 0, Math.PI*2);
            ctx.fill();
        }

        ctx.restore();
    }

    initBgParticles();
    gameLoop();
</script>
</body>
</html>
"""

# Streamlit Component를 사용하여 HTML 코드 렌더링
components.html(game_html, height=750, scrolling=False)
