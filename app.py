import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Gravity Arrow: Planetary Journey")

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
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            user-select: none;
        }
        #game-container {
            position: relative;
            width: 1000px;
            height: 650px;
            margin-top: 10px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            border-radius: 16px;
            overflow: hidden;
            border: 2px solid #334155;
        }
        canvas {
            background: transparent;
            display: block;
        }
        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 20px;
            box-sizing: border-box;
        }
        .interactive {
            pointer-events: auto;
        }
        #header-info {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            width: 100%;
        }
        .glass-panel {
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px 24px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        #score-box h1 {
            margin: 0;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #94a3b8;
        }
        #score-disp {
            font-size: 38px;
            font-weight: 800;
            margin: 0;
            color: #38bdf8;
            text-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
        }
        #planet-selector {
            display: flex;
            gap: 12px;
        }
        .planet-btn {
            background: rgba(30, 41, 59, 0.7);
            border: 2px solid #475569;
            border-radius: 50%;
            width: 56px;
            height: 56px;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            padding: 0;
            overflow: hidden;
        }
        .planet-btn:hover {
            transform: scale(1.12);
            border-color: #38bdf8;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
        }
        .planet-btn.active {
            border-color: #0ea5e9;
            background: rgba(14, 165, 233, 0.15);
            box-shadow: 0 0 20px rgba(14, 165, 233, 0.5);
            transform: scale(1.05);
        }
        .planet-canvas {
            width: 100%;
            height: 100%;
            border-radius: 50%;
        }
        #combo-wrapper {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -120%) scale(1);
            text-align: center;
            transition: all 0.2s ease-out;
        }
        #combo-disp {
            font-size: 46px;
            font-weight: 900;
            font-style: italic;
            color: #f43f5e;
            text-shadow: 0 0 16px rgba(244, 63, 94, 0.6), 0 4px 6px rgba(0,0,0,0.4);
            margin: 0;
            animation: pulse 0.4s ease-out infinite alternate;
        }
        @keyframes pulse {
            0% { transform: scale(0.96); }
            100% { transform: scale(1.04); }
        }
        .hidden {
            display: none !important;
            opacity: 0;
        }
        #ammo-status {
            position: absolute;
            bottom: 30px;
            left: 40px;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        }
        .indicator-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
        }
        .ready-dot { background-color: #10b981; box-shadow: 0 0 10px #10b981; }
        .reload-dot { background-color: #ef4444; box-shadow: 0 0 10px #ef4444; animation: blink 0.5s infinite alternate; }
        @keyframes blink { 0% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
</head>
<body>

    <div id="game-container">
        <canvas id="gameCanvas" width="1000" height="650"></canvas>
        
        <div id="ui-layer">
            <div id="header-info">
                <div id="score-box" class="glass-panel">
                    <h1>Score</h1>
                    <p id="score-disp">0</p>
                </div>
                
                <div id="planet-selector" class="interactive">
                    <button class="planet-btn active" onclick="selectPlanet('earth')" id="btn-earth"></button>
                    <button class="planet-btn" onclick="selectPlanet('moon')" id="btn-moon"></button>
                    <button class="planet-btn" onclick="selectPlanet('mars')" id="btn-mars"></button>
                    <button class="planet-btn" onclick="selectPlanet('venus')" id="btn-venus"></button>
                    <button class="planet-btn" onclick="selectPlanet('europa')" id="btn-europa"></button>
                </div>
            </div>
            
            <div id="combo-wrapper" class="hidden">
                <p id="combo-disp">1 COMBO</p>
            </div>

            <div id="ammo-status" class="glass-panel">
                <span id="ammo-dot" class="indicator-dot ready-dot"></span>
                <span id="ammo-text" style="color: #e2e8f0;">READY</span>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // 게임 기본 관리 상태 인자 배열 정의
        let score = 0;
        let combo = 0;
        let maxCombo = 0;
        let gameActive = true;

        // 행성 스펙 정의 오브젝트 리스트
        const planets = {
            earth: { gravity: 0.45, color: '#3b82f6', name: '지구' },
            moon: { gravity: 0.08, color: '#94a3b8', name: '달' },
            mars: { gravity: 0.18, color: '#f97316', name: '화성' },
            venus: { gravity: 0.40, color: '#eab308', name: '금성' },
            europa: { gravity: 0.06, color: '#22d3ee', name: '유로파' }
        };
        let currentPlanetKey = 'earth';
        let currentGravity = planets.earth.gravity;

        // 조작 조준점 물리 벡터 공간 설정
        const bowPos = { x: 130, y: 380 };
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let dragEnd = { x: 0, y: 0 };

        // [화살 재장전 기믹 추가 변수]
        let isArrowInFlight = false; 
        let reloadTimer = 0;        

        // 오브젝트 풀링 제어 바인딩 배열성 구조화
        let activeArrows = [];
        let particles = [];
        let scoreTexts = [];
        let stars = [];
        
        // 환경 특수 이펙트 변수 풀
        let clouds = [];
        let environmentParticles = []; 
        let venusPhase = 0;

        // 과녁 구조 정의서 형성
        let target = {
            x: 820, y: 300,
            speed: 2.5, dir: 1,
            visible: true, respawnTimer: 0,
            radiusD: 55, radiusC: 40, radiusB: 25, radiusA: 10
        };

        // 특수 이벤트 요소: 운석 정의
        let meteor = { x: 0, y: 0, vx: 0, vy: 0, radius: 26, active: false, destroyed: false };
        let gameFrameCount = 0;

        // 각성 버프 제어 장치 시스템
        let isBuffed = false;
        let buffTimer = 0;
        const maxBuffDuration = 480; 

        // 사과 화살 전용 가이드라인 트리거 시스템 
        let currentArrow = { isApple: false };
        let appleTimer = 0;
        let appleTrajectoryVisible = true;

        let shakeIntensity = 0;

        // 초기 실행 분기점 환경 설정 진입구
        function init() {
            // 성운/별 배경 난수 분포 생성
            stars = [];
            for(let i=0; i<120; i++) {
                stars.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    r: Math.random() * 1.8 + 0.4
                });
            }

            // 지구 전용 구름 데이터 초기 세팅
            clouds = [];
            for(let i=0; i<5; i++) {
                clouds.push({
                    x: Math.random() * canvas.width,
                    y: 50 + Math.random() * 120,
                    speed: 0.2 + Math.random() * 0.4,
                    scale: 0.6 + Math.random() * 0.7
                });
            }

            // 환경 입자 초기 풀 생성 (눈, 먼지 공용)
            environmentParticles = [];
            for(let i=0; i<80; i++) {
                environmentParticles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.5,
                    vy: Math.random() * 1.5 + 0.5,
                    size: Math.random() * 2.5 + 1,
                    alpha: Math.random() * 0.6 + 0.2
                });
            }

            drawPlanetButtons();
            
            // 마우스 및 터치 이벤트 리스너 핸들링 등록 교정
            canvas.addEventListener('mousedown', onMouseDown);
            canvas.addEventListener('mousemove', onMouseMove);
            window.addEventListener('mouseup', onMouseUp);
        }

        // 행성별 미니 버튼 커스텀 UI 생성기 (요청 사양 반영)
        function drawPlanetButtons() {
            Object.keys(planets).forEach(key => {
                const btn = document.getElementById(`btn-${key}`);
                if (!btn) return;
                
                // 버튼 내부에 렌더링용 전용 캔버스 생성 배포
                btn.innerHTML = '';
                const pCanvas = document.createElement('canvas');
                pCanvas.className = 'planet-canvas';
                pCanvas.width = 100;
                pCanvas.height = 100;
                btn.appendChild(pCanvas);
                
                const pCtx = pCanvas.getContext('2d');
                pCtx.clearRect(0,0,100,100);
                
                if (key === 'earth') {
                    // 지구: 초록색 육지, 파란색 바다
                    pCtx.fillStyle = '#1e3a8a';
                    pCtx.beginPath(); pCtx.arc(50,50,45,0,Math.PI*2); pCtx.fill();
                    pCtx.fillStyle = '#15803d';
                    pCtx.beginPath(); pCtx.arc(38,42,16,0,Math.PI*2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(65,58,22,0,Math.PI*2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(42,68,12,0,Math.PI*2); pCtx.fill();
                } else if (key === 'moon') {
                    // 달: 회색에 검은색 자국들
                    pCtx.fillStyle = '#94a3b8';
                    pCtx.beginPath(); pCtx.arc(50,50,45,0,Math.PI*2); pCtx.fill();
                    pCtx.fillStyle = '#475569';
                    pCtx.beginPath(); pCtx.arc(35,35,10,0,Math.PI*2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(62,45,14,0,Math.PI*2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(45,68,8,0,Math.PI*2); pCtx.fill();
                } else if (key === 'mars') {
                    // 화성: 주황색에 갈색 반점
                    pCtx.fillStyle = '#ea580c';
                    pCtx.beginPath(); pCtx.arc(50,50,45,0,Math.PI*2); pCtx.fill();
                    pCtx.fillStyle = '#7c2d12';
                    pCtx.beginPath(); pCtx.arc(40,52,14,0,Math.PI*2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(68,38,11,0,Math.PI*2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(52,68,7,0,Math.PI*2); pCtx.fill();
                } else if (key === 'venus') {
                    // 금성: 노란색에 진노란색 반점
                    pCtx.fillStyle = '#eab308';
                    pCtx.beginPath(); pCtx.arc(50,50,45,0,Math.PI*2); pCtx.fill();
                    pCtx.fillStyle = '#a16207';
                    pCtx.beginPath(); pCtx.arc(32,44,12,0,Math.PI*2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(58,62,15,0,Math.PI*2); pCtx.fill();
                    pCtx.beginPath(); pCtx.arc(64,34,9,0,Math.PI*2); pCtx.fill();
                } else if (key === 'europa') {
                    // 유로파: 청백색 및 빙하 균열 원형 유지
                    pCtx.fillStyle = '#bae6fd';
                    pCtx.beginPath(); pCtx.arc(50,50,45,0,Math.PI*2); pCtx.fill();
                    pCtx.strokeStyle = '#0284c7'; pCtx.lineWidth = 3;
                    pCtx.beginPath(); pCtx.moveTo(20,40); pCtx.lineTo(50,70); pCtx.lineTo(80,50); pCtx.stroke();
                    pCtx.beginPath(); pCtx.moveTo(40,22); pCtx.lineTo(65,54); pCtx.stroke();
                }
            });
        }

        // 행성 선택 트리거 스위칭 장치 연동
        function selectPlanet(key) {
            currentPlanetKey = key;
            currentGravity = planets[key].gravity;
            
            document.querySelectorAll('.planet-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`btn-${key}`).classList.add('active');

            // 화성/금성 전환 시 환경 파티클 방향성 리셋 보정 연산
            if(key === 'venus') {
                environmentParticles.forEach(p => {
                    p.vx = -(Math.random() * 2.5 + 1.5);
                    p.vy = (Math.random() - 0.5) * 0.4;
                });
            } else if(key === 'mars') {
                environmentParticles.forEach(p => {
                    p.vx = (Math.random() - 0.5) * 0.6;
                    p.vy = (Math.random() - 0.5) * 0.5;
                });
            } else if(key === 'europa') {
                environmentParticles.forEach(p => {
                    p.vx = (Math.random() - 0.3) * 0.5;
                    p.vy = Math.random() * 1.8 + 0.8;
                });
            }
        }

        function onMouseDown(e) {
            // [화살 비행 중이거나 재장전 대기 중일 때는 조작 불가 조치]
            if(!gameActive || isArrowInFlight) return;

            const rect = canvas.getBoundingClientRect();
            const mX = e.clientX - rect.left;
            const mY = e.clientY - rect.top;

            // 활 캐릭터 반경 내 조작 드래그 유효성 체크 판정 진행
            if (Math.hypot(mX - bowPos.x, mY - bowPos.y) < 90) {
                isDragging = true;
                dragStart = { x: bowPos.x, y: bowPos.y };
                dragEnd = { x: mX, y: mY };
            }
        }

        function onMouseMove(e) {
            if (!isDragging) return;
            const rect = canvas.getBoundingClientRect();
            dragEnd.x = e.clientX - rect.left;
            dragEnd.y = e.clientY - rect.top;
        }

        function onMouseUp(e) {
            if (!isDragging) return;
            isDragging = false;

            let pVx = (dragStart.x - dragEnd.x) * 0.25;
            let pVy = (dragStart.y - dragEnd.y) * 0.25;

            // 투사 방향이 전방향성을 지닐 때만 발사 판정 처리 인정 고수
            if (pVx > 0.5) {
                activeArrows.push({
                    x: bowPos.x,
                    y: bowPos.y,
                    vx: pVx,
                    vy: pVy,
                    width: 95,
                    isApple: currentArrow.isApple,
                    handled: false
                });

                // [발사 시 비행 모드 온으로 변경하여 재배치 락다운 처리 가동]
                isArrowInFlight = true;
                updateAmmoStatus(false);

                // 발사 직후 확률 연산 기믹에 근거한 사과 화살 룰렛 재갱신 가동
                currentArrow.isApple = Math.random() < 0.22;
            }
        }

        // 암모 상단 인터페이스 연동 제어 함수 추가
        function updateAmmoStatus(ready) {
            const dot = document.getElementById('ammo-dot');
            const txt = document.getElementById('ammo-text');
            if(!dot || !txt) return;

            if(ready) {
                dot.className = "indicator-dot ready-dot";
                txt.innerText = "READY";
            } else {
                dot.className = "indicator-dot reload-dot";
                txt.innerText = "RELOADING...";
            }
        }

        // 특수 이벤트 연출용 파티클 생성기
        function createExplosion(x, y, color, count) {
            for (let i = 0; i < count; i++) {
                let angle = Math.random() * Math.PI * 2;
                let speed = Math.random() * 5 + 2;
                particles.push({
                    x: x, y: y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    radius: Math.random() * 3.5 + 1.2,
                    color: color,
                    alpha: 1,
                    decay: Math.random() * 0.02 + 0.015
                });
            }
        }

        function createScoreText(x, y, text, color) {
            scoreTexts.push({ x: x, y: y, text: text, color: color, alpha: 1, vy: -0.9 });
        }

        // 버프 패시브 온 연산 모듈 정의
        function activateAbilityBuff() {
            isBuffed = true;
            buffTimer = maxBuffDuration;
            appleTrajectoryVisible = true; 
        }

        function deactivateAbilityBuff() {
            isBuffed = false;
        }

        // 궁수 캐릭터 메인 드로잉 로직 구현
        function drawArcherCharacter(angle) {
            ctx.save();
            ctx.translate(bowPos.x - 35, bowPos.y + 15);
            
            // 몸체 실루엣 드로잉
            ctx.fillStyle = "#1e293b";
            ctx.beginPath();
            ctx.moveTo(-15, 40); ctx.lineTo(15, 40); ctx.lineTo(10, -20); ctx.lineTo(-10, -20);
            ctx.closePath(); ctx.fill();

            // 머리 부분 렌더링
            ctx.fillStyle = "#334155";
            ctx.beginPath(); ctx.arc(0, -34, 14, 0, Math.PI*2); ctx.fill();

            // 조준 방향 연동 숄더 암 트래킹 연산 처리
            ctx.translate(20, -15);
            ctx.rotate(angle);
            ctx.fillStyle = isBuffed ? "#f43f5e" : "#38bdf8";
            ctx.fillRect(0, -5, 35, 10);
            ctx.restore();
        }

        function drawEarthBackground() {
            // 하늘색 배경 그라데이션 형성
            let skyGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
            skyGrad.addColorStop(0, '#bae6fd');
            skyGrad.addColorStop(1, '#e0f2fe');
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 유유히 흘러가는 구름 시각화
            ctx.fillStyle = "rgba(255, 255, 255, 0.75)";
            clouds.forEach(c => {
                c.x += c.speed;
                if(c.x > canvas.width + 100) c.x = -100;
                
                ctx.save();
                ctx.translate(c.x, c.y);
                ctx.scale(c.scale, c.scale);
                ctx.beginPath();
                ctx.arc(0, 0, 25, 0, Math.PI*2);
                ctx.arc(20, -10, 30, 0, Math.PI*2);
                ctx.arc(45, 0, 22, 0, Math.PI*2);
                ctx.arc(20, 10, 25, 0, Math.PI*2);
                ctx.fill();
                ctx.restore();
            });

            // 하단 평평한 갈색 땅 지형 렌더링
            ctx.fillStyle = '#854d0e';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 40);
            ctx.fillStyle = '#166534';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 8);
        }

        function drawMoonBackground() {
            // 달의 어두운 우주 배경 처리
            ctx.fillStyle = '#000000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 우주 성운 입자 시각화 잔류 노출
            ctx.fillStyle = "rgba(255,255,255,0.45)";
            stars.forEach(s => {
                ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill();
            });

            // 울퉁불퉁한 회색 표면 바닥 지형 드로잉 처리
            ctx.fillStyle = '#475569';
            ctx.beginPath();
            ctx.moveTo(0, canvas.height);
            ctx.lineTo(0, canvas.height - 50);
            
            // 크레이터 형태를 대변하는 굴곡 사인곡선 복합 제어 루프 연산
            for(let i=0; i<=canvas.width; i+=40) {
                let yOffset = Math.sin(i * 0.05) * 8 + Math.cos(i * 0.02) * 6;
                if(i % 120 === 0) yOffset -= 12; // 간이 크레이터 파임 홈 연출
                ctx.lineTo(i, canvas.height - 42 + yOffset);
            }
            ctx.lineTo(canvas.width, canvas.height);
            ctx.closePath();
            ctx.fill();

            // 바닥 내부 크레이터 음영 추가 디테일링
            ctx.fillStyle = '#334155';
            for(let i=60; i<canvas.width; i+=180) {
                ctx.beginPath();
                ctx.ellipse(i, canvas.height - 25, 20, 6, 0, 0, Math.PI*2);
                ctx.fill();
            }
        }

        function drawMarsBackground() {
            // 뿌연 노란색/오렌지빛 하늘 대기 상태 연출 그라데이션
            let marsGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
            marsGrad.addColorStop(0, '#fef08a');
            marsGrad.addColorStop(0.6, '#fed7aa');
            marsGrad.addColorStop(1, '#ffedd5');
            ctx.fillStyle = marsGrad;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 대기 중 흩날리는 부유 먼지 파티클 연산 처리 고동 가동
            ctx.fillStyle = "rgba(194, 65, 12, 0.22)";
            environmentParticles.forEach(p => {
                p.x += p.vx; p.y += p.vy;
                if(p.x < 0) p.x = canvas.width;
                if(p.x > canvas.width) p.x = 0;
                if(p.y > canvas.height) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * 1.5, 0, Math.PI*2);
                ctx.fill();
            });

            // 갈색 대지 바닥면 그리기
            ctx.fillStyle = '#7c2d12';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 40);
            ctx.fillStyle = '#9a3412';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 6);
        }

        function drawVenusBackground() {
            // 진노란색 스모그 가득한 기본 배경 베이스 드로잉
            ctx.fillStyle = '#fef08a';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 먼지 스톰 흐름 제어를 위한 페이즈 누적 상수 연산
            venusPhase += 0.01;

            // 오른쪽에서 왼쪽으로 거세게 흐르는 먼지 폭풍 기류 트레일 드로잉 연출 구문
            ctx.strokeStyle = "rgba(161, 98, 7, 0.12)";
            ctx.lineWidth = 4;
            for(let i=0; i<25; i++) {
                let yPos = (i * 26 + venusPhase * 40) % canvas.height;
                ctx.beginPath();
                ctx.moveTo(canvas.width + 50, yPos);
                ctx.lineTo(-50, yPos + Math.sin(venusPhase + i)*20);
                ctx.stroke();
            }

            // 고속 표면 이동 입자 연산
            ctx.fillStyle = "rgba(113, 63, 4, 0.35)";
            environmentParticles.forEach(p => {
                p.x += p.vx * 1.8; 
                p.y += p.vy * 0.5;
                if(p.x < -20) p.x = canvas.width + 20;
                if(p.y > canvas.height) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * 1.1, 0, Math.PI*2);
                ctx.fill();
            });

            // 대기 먼지 효과용 뿌연 반투명 필터 상단 스크린 레이어 레이아웃 오버랩 진행
            ctx.fillStyle = "rgba(234, 179, 8, 0.18)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 노란색 지표면 바닥 드로잉
            ctx.fillStyle = '#ca8a04';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 40);
            ctx.fillStyle = '#854d0e';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 5);
        }

        function drawEuropaBackground() {
            // 뿌연 하늘색 대기 연출
            let euroGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
            euroGrad.addColorStop(0, '#a5f3fc');
            euroGrad.addColorStop(1, '#ecfeff');
            ctx.fillStyle = euroGrad;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 금이 가있는 빙판 바닥 지형 렌더링 구현
            ctx.fillStyle = '#e0f2fe';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 40);

            // 빙판 표면 스트레스 크랙(균열선) 세부 묘사 렌더 프로시저
            ctx.strokeStyle = '#0284c7';
            ctx.lineWidth = 2.5;
            
            ctx.save();
            ctx.beginPath();
            // 임의 크랙 패스 기하학적 수치 고정 드로잉 진행
            ctx.moveTo(0, canvas.height - 30); ctx.lineTo(180, canvas.height - 10); ctx.lineTo(340, canvas.height - 35);
            ctx.moveTo(250, canvas.height - 20); ctx.lineTo(290, canvas.height);
            ctx.moveTo(500, canvas.height - 40); ctx.lineTo(560, canvas.height - 5); ctx.lineTo(720, canvas.height - 25);
            ctx.moveTo(680, canvas.height - 28); ctx.lineTo(800, canvas.height - 2); ctx.lineTo(1000, canvas.height - 20);
            ctx.stroke();
            ctx.restore();

            // 지속적으로 계속 내리는 눈(Snowfall) 입자 물리 연산 시각화 처리구간 반영
            ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
            environmentParticles.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;
                if(p.y > canvas.height - 40) {
                    p.y = 0;
                    p.x = Math.random() * canvas.width;
                }
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
                ctx.fill();
            });
        }

        function update() {
            // 능력치 유지시간 프레임 차감 연산 진행
            if (gameActive && isBuffed) {
                buffTimer--;
                if(buffTimer <= 0) {
                    deactivateAbilityBuff();
                }
            }

            // [재장전 타이머 진행 연산 기믹 탑재]
            if (reloadTimer > 0) {
                reloadTimer--;
                if (reloadTimer <= 0) {
                    isArrowInFlight = false; // 타임아웃 완료 시 조작 연동 봉인 해제 진행
                    updateAmmoStatus(true);
                }
            }

            if (gameActive) {
                gameFrameCount++;
                
                // 15초(900프레임) 단위 마다 규칙적 운석 기습 이벤트 생성 처리기 가동
                if(gameFrameCount % 900 === 0 && !meteor.active) {
                    meteor.x = canvas.width + 40;
                    meteor.y = 100 + Math.random() * 200;
                    meteor.vx = -(Math.random() * 2.5 + 3.0);
                    meteor.vy = Math.random() * 0.8;
                    meteor.active = true;
                    meteor.destroyed = false;
                }

                // 과녁이 살아있을 때만 움직임 가동
                if(target.visible) {
                    target.y += target.speed * target.dir;
                    if(target.y - target.radiusD < 140 || target.y + target.radiusD > canvas.height - 40) {
                        target.dir *= -1; 
                    }
                } else {
                    // 과녁 소멸 리스폰 대기 연산 타이머 작동 처리
                    target.respawnTimer--;
                    if(target.respawnTimer <= 0) {
                        target.y = 180 + Math.random() * (canvas.height - 320);
                        target.visible = true;
                    }
                }

                // 사과 화살 깜빡이 갱신
                if(currentArrow.isApple) {
                    appleTimer++;
                    if(appleTimer % 45 === 0) {
                        appleTrajectoryVisible = !appleTrajectoryVisible;
                    }
                }

                // 운석 이동 물리엔진 연산구간
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
            if (shakeIntensity > 0) {
                ctx.translate((Math.random() - 0.5) * shakeIntensity, (Math.random() - 0.5) * shakeIntensity);
                shakeIntensity *= 0.85; 
                if (shakeIntensity < 0.2) shakeIntensity = 0;
            }

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // [선택 행성별 스위칭 기반 백그라운드 환경 드로잉 위임 분기]
            if (currentPlanetKey === 'earth') drawEarthBackground();
            else if (currentPlanetKey === 'moon') drawMoonBackground();
            else if (currentPlanetKey === 'mars') drawMarsBackground();
            else if (currentPlanetKey === 'venus') drawVenusBackground();
            else if (currentPlanetKey === 'europa') drawEuropaBackground();

            // 각성 버프 모드 돌입 시 붉은색 스크린 연출 처리 필터링
            if(isBuffed && gameActive) {
                ctx.fillStyle = "rgba(255, 62, 62, 0.04)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            // [운석(Meteor) 그리기 섹션]
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

            // [과녁 렌더링 - 원형 유지 설계]
            const targetColor = planets[currentPlanetKey].color;
            const skewX = 0.25; 
            const frontX = target.x - (target.radiusD * skewX); 
            const backX = target.x + (target.radiusD * skewX); 

            if(target.visible) {
                ctx.save();
                ctx.strokeStyle = "#4a5568"; ctx.lineWidth = 6;
                ctx.beginPath();
                ctx.moveTo(target.x + 5, target.y - target.radiusD); ctx.lineTo(target.x + 5, target.y + target.radiusD);
                ctx.stroke();

                ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, (target.radiusD + 6) * skewX, target.radiusD + 6, 0, 0, Math.PI * 2); ctx.fill();

                ctx.fillStyle = "#ffffff";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2); ctx.fill(); 
                
                ctx.fillStyle = targetColor;
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusC * skewX, target.radiusC, 0, 0, Math.PI * 2); ctx.fill();
                
                ctx.fillStyle = "#ff3e3e";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusB * skewX, target.radiusB, 0, 0, Math.PI * 2); ctx.fill();
                
                ctx.fillStyle = "#ffcc00";
                ctx.beginPath(); ctx.ellipse(target.x, target.y, target.radiusA * skewX, target.radiusA, 0, 0, Math.PI * 2); ctx.fill();
                ctx.restore();
            }

            // 캐릭터 원형 레이아웃 유지 드로잉 호출
            let dragAngle = Math.atan2(dragStart.y - dragEnd.y, dragStart.x - dragEnd.x);
            drawArcherCharacter(dragAngle);

            // 활과 활시위 레이아웃 드로잉 포지션 업데이트 보정
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

            // [비행 중이거나 대기 중이 아닐 때만 대기용 화살 노출]
            if(!isDragging && gameActive && !isArrowInFlight) {
                drawArrowIcon(bowPos.x, bowPos.y, 0, currentArrow.isApple);
            }

            // 포물선 가이드라인 궤적 트래킹 연산 루프
            if (isDragging && appleTrajectoryVisible && gameActive) {
                let tVx = (dragStart.x - dragEnd.x) * 0.25;
                if (tVx > 0) { 
                    ctx.save();
                    ctx.strokeStyle = currentArrow.isApple ? "#af0404" : "rgba(0, 210, 255, 0.5)";
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

            // 화살 배열 투사체 순회 및 처리구간
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                arrow.x += arrow.vx;
                arrow.y += arrow.vy;
                arrow.vy += currentGravity;

                let arrowAngle = Math.atan2(arrow.vy, arrow.vx);
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.isApple, arrow.width);

                let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);

                // [탈출 Miss 조건 판정]: 화면 경계 바깥 탈출 스캔 검사 연산 처리
                if (arrow.x > canvas.width + 50 || arrow.y > canvas.height + 50 || arrow.y < -50) {
                    if(!arrow.handled) {
                        combo = 0; document.getElementById('combo-wrapper').classList.add('hidden');
                        
                        // [요청 연동]: 과녁을 맞추지 못하고 나가면 사라진 뒤 1초(60프레임) 디레이 타이머 작동 가동
                        reloadTimer = 60; 
                    }
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 충돌 처리 루프 1단계: 특수 운석 충돌 트래킹 검증
                if(meteor.active) {
                    let distToMeteor = Math.hypot(arrowTipX - meteor.x, arrowTipY - meteor.y);
                    if(distToMeteor <= meteor.radius + 10) {
                        meteor.active = false;
                        meteor.destroyed = true;
                        activeArrows.splice(i, 1); 

                        createExplosion(meteor.x, meteor.y, "#ffcc00", 40);
                        createScoreText(meteor.x, meteor.y, "AWAKENING!!", "#ffcc00");
                        
                        activateAbilityBuff();

                        // 운석 타격 성공 시에도 화살 회수 연동 바로 가동 유도 허용
                        isArrowInFlight = false;
                        updateAmmoStatus(true);
                        continue;
                    }
                }

                // 충돌 처리 루프 2단계: 메인 과녁 충돌 트래킹 감지 검사
                if (target.visible && arrowTipX >= frontX && arrowTipX <= backX + 15 && arrow.vx > 0) {
                    let dy = Math.abs(arrowTipY - target.y);

                    if (dy <= target.radiusD) {
                        arrow.handled = true;
                        
                        target.visible = false;
                        target.respawnTimer = 45; 

                        combo++;
                        if(combo > maxCombo) maxCombo = combo;
                        
                        document.getElementById('combo-disp').innerText = `${combo} COMBO`;
                        document.getElementById('combo-wrapper').classList.remove('hidden');

                        let earnedPoints = 0;
                        let hColor = "#ffffff";
                        
                        if (dy <= target.radiusA) { earnedPoints = 10; hColor = "#ffcc00"; }
                        else if (dy <= target.radiusB) { earnedPoints = 5;  hColor = "#ff3e3e"; }
                        else if (dy <= target.radiusC) { earnedPoints = 2;  hColor = targetColor; }
                        else { earnedPoints = 1;  hColor = "#e2e8f0"; }

                        if(arrow.isApple) { earnedPoints *= 2; hColor = "#ff2222"; }

                        let totalEarned = earnedPoints + Math.floor(combo / 3);
                        score += totalEarned;
                        document.getElementById('score-disp').innerText = score;

                        createScoreText(arrowTipX - 25, arrowTipY - 15, `+${totalEarned}`, hColor);
                        shakeIntensity = 7; 
                        createExplosion(arrowTipX, arrowTipY, hColor, 20);

                        activeArrows.splice(i, 1); 

                        // [요청 사양 반영]: 과녁 명중 시 즉시 화살 장전 가동 활성화 처리
                        isArrowInFlight = false;
                        updateAmmoStatus(true);
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

            // 스코어 부유 텍스트
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

            if(isApple) {
                ctx.fillStyle = "#fa5252"; ctx.beginPath(); ctx.arc(0, -4, 11, 0, Math.PI*2); ctx.fill();
                ctx.strokeStyle = "#868e96"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, -14); ctx.quadraticCurveTo(3, -19, 6, -17); ctx.stroke();
            }
            ctx.restore();
        }

        init();
        update();
    </script>
</body>
</html>
"""

components.html(game_html, height=700, scrolling=False)
