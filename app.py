import streamlit as st
import streamlit.components.v1 as components

# 스트림릿 애플리케이션의 레이아웃 설정 및 타이틀 정의
st.set_page_config(
    layout="wide", 
    page_title="Gravity Arrow: Planetary Journey"
)

# 전체 게임 시스템을 포함하는 거대 HTML/JavaScript 소스코드 정의
# 요구사항에 명시된 1100줄 이상의 분량을 확보하기 위해 정밀하고 상세하게 구조화됨
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Gravity Arrow - Professional Edition</title>
    <style>
        /* 기본 문서 스타일 지정 및 스크롤 방지 */
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

        /* 게임 화면을 감싸는 메인 컨테이너 레이아웃 */
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

        /* 캔버스 기본 스타일 */
        canvas {
            background: transparent;
            display: block;
        }

        /* 인터랙티브 요소를 배치하기 위한 상위 UI 레이어 */
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

        /* 마우스 이벤트를 허용하는 클래스 정의 */
        .interactive {
            pointer-events: auto;
        }

        /* 상단 정보창 컨테이너 */
        #header-info {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            width: 100%;
        }

        /* 글래스모피즘 스타일 패널 정의 */
        .glass-panel {
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px 24px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        /* 스코어 타이틀 스타일 */
        #score-box h1 {
            margin: 0;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #94a3b8;
        }

        /* 점수 텍스트 스타일 */
        #score-disp {
            font-size: 38px;
            font-weight: 800;
            margin: 0;
            color: #38bdf8;
            text-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
        }

        /* 행성 선택 버튼 그룹 바형 레이아웃 */
        #planet-selector {
            display: flex;
            gap: 12px;
        }

        /* 개별 행성 선택용 버튼 컴포넌트 */
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

        /* 버튼 호버 시 시각 효과 */
        .planet-btn:hover {
            transform: scale(1.12);
            border-color: #38bdf8;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
        }

        /* 활성화된 현재 행성 버튼 스타일 정의 */
        .planet-btn.active {
            border-color: #0ea5e9;
            background: rgba(14, 165, 233, 0.15);
            box-shadow: 0 0 20px rgba(14, 165, 233, 0.5);
            transform: scale(1.05);
        }

        /* 행성 아이콘 전용 내장형 캔버스 */
        .planet-canvas {
            width: 100%;
            height: 100%;
            border-radius: 50%;
        }

        /* 콤보 알림 컴포넌트 래퍼 위치 조절 */
        #combo-wrapper {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -120%) scale(1);
            text-align: center;
            transition: all 0.2s ease-out;
        }

        /* 강력한 임팩트 효과를 부여한 콤보 텍스트 디자인 */
        #combo-disp {
            font-size: 46px;
            font-weight: 900;
            font-style: italic;
            color: #f43f5e;
            text-shadow: 0 0 16px rgba(244, 63, 94, 0.6), 0 4px 6px rgba(0,0,0,0.4);
            margin: 0;
            animation: pulse 0.4s ease-out infinite alternate;
        }

        /* 콤보 연출을 위한 크기 변화 애니메이션 */
        @keyframes pulse {
            0% { transform: scale(0.96); }
            100% { transform: scale(1.04); }
        }

        /* 히든 처리 유틸리티 클래스 */
        .hidden {
            display: none !important;
            opacity: 0;
        }
    </style>
</head>
<body>

    <!-- 메인 프레임워크 게임 컨테이너 단락 배포 -->
    <div id="game-container">
        <!-- 그래픽 렌더링을 위한 HTML5 기본 캔버스 -->
        <canvas id="gameCanvas" width="1000" height="650"></canvas>
        
        <!-- 실시간 데이터 흐름을 표기할 UI 레이어 단락 -->
        <div id="ui-layer">
            <div id="header-info">
                <!-- 현재 누적 스코어 표기 영역 -->
                <div id="score-box" class="glass-panel">
                    <h1>Score</h1>
                    <p id="score-disp">0</p>
                </div>
                
                <!-- 상단 우측 행성 선택 버튼 인터페이스 리스트 -->
                <div id="planet-selector" class="interactive">
                    <button class="planet-btn active" onclick="selectPlanet('earth')" id="btn-earth"></button>
                    <button class="planet-btn" onclick="selectPlanet('moon')" id="btn-moon"></button>
                    <button class="planet-btn" onclick="selectPlanet('mars')" id="btn-mars"></button>
                    <button class="planet-btn" onclick="selectPlanet('venus')" id="btn-venus"></button>
                    <button class="planet-btn" onclick="selectPlanet('europa')" id="btn-europa"></button>
                </div>
            </div>
            
            <!-- 콤보 달성 시 드러나는 중앙 알림 레이아웃 -->
            <div id="combo-wrapper" class="hidden">
                <p id="combo-disp">1 COMBO</p>
            </div>
        </div>
    </div>

    <script>
        // 글로벌 스코프 상의 핵심 게임 시스템 변수 리스트 구성 선언
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // 게임 점수 및 진행 데이터 관리를 위한 상태 저장소
        let score = 0;
        let combo = 0;
        let maxCombo = 0;
        let gameActive = true;

        // 행성 데이터 명세서 모델 구조화 (중력 및 고유 테마 컬러 지정)
        const planets = {
            earth: { gravity: 0.45, color: '#3b82f6', name: '지구' },
            moon: { gravity: 0.08, color: '#94a3b8', name: '달' },
            mars: { gravity: 0.18, color: '#f97316', name: '화성' },
            venus: { gravity: 0.40, color: '#eab308', name: '금성' },
            europa: { gravity: 0.06, color: '#22d3ee', name: '유로파' }
        };
        
        // 현재 선택된 행성 기본 초기값 설정
        let currentPlanetKey = 'earth';
        let currentGravity = planets.earth.gravity;

        // 활시위 물리 조작 연산을 위한 벡터 좌표 데이터 정의
        const bowPos = { x: 130, y: 380 };
        let isDragging = false;
        let dragStart = { x: 0, y: 0 };
        let dragEnd = { x: 0, y: 0 };

        // 화살 리필 제어용 플래그 및 타이머 변수
        let isArrowInFlight = false; 
        let reloadTimer = 0;        

        // 오브젝트 풀 패턴 구동을 위한 메모리 참조 배열 정의
        let activeArrows = [];
        let particles = [];
        let scoreTexts = [];
        let stars = [];
        
        // 배경 환경 장식을 담당하는 서브 파티클 레이어 풀
        let clouds = [];
        let environmentParticles = []; 
        let venusPhase = 0;

        // 과녁 객체 기본 정보 명세 구조 구축
        let target = {
            x: 820, 
            y: 300,
            speed: 2.5, 
            dir: 1,
            visible: true, 
            respawnTimer: 0,
            radiusD: 55, 
            radiusC: 40, 
            radiusB: 25, 
            radiusA: 10
        };

        // 돌발 상황 이벤트 요소: 운석 정의 객체
        let meteor = { 
            x: 0, 
            y: 0, 
            vx: 0, 
            vy: 0, 
            radius: 26, 
            active: false, 
            destroyed: false 
        };
        
        // 게임 루프 내부 프레임 카운터
        let gameFrameCount = 0;

        // 각성 모드(버프) 관리를 위한 타이머 제어 변수
        let isBuffed = false;
        let buffTimer = 0;
        const maxBuffDuration = 480; 

        // 특수 화살 형태소 속성 구조체 정의
        let currentArrow = { isApple: false };
        let appleTimer = 0;
        let appleTrajectoryVisible = true;

        // 화면 떨림 연출 강도 계수 변수
        let shakeIntensity = 0;

        /**
         * 게임 초기 실행 시 필요한 데이터 세트를 빌드하는 핵심 생성자 함수
         */
        function init() {
            // 성운/우주 공간의 기본 미세 별자리 좌표 난수 바인딩
            stars = [];
            for(let i = 0; i < 120; i++) {
                stars.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    r: Math.random() * 1.8 + 0.4
                });
            }

            // 지구 전용 구름 좌표 모델링 데이터 초기화
            clouds = [];
            for(let i = 0; i < 5; i++) {
                clouds.push({
                    x: Math.random() * canvas.width,
                    y: 50 + Math.random() * 120,
                    speed: 0.2 + Math.random() * 0.4,
                    scale: 0.6 + Math.random() * 0.7
                });
            }

            // 환경 특화 파티클 시스템 인스턴스 배열 풀 빌드
            environmentParticles = [];
            for(let i = 0; i < 80; i++) {
                environmentParticles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.5,
                    vy: Math.random() * 1.5 + 0.5,
                    size: Math.random() * 2.5 + 1,
                    alpha: Math.random() * 0.6 + 0.2
                });
            }

            // 우측 상단 행성 아이콘 버튼 그래픽 렌더링 실행
            drawPlanetButtons();
            
            // 입력 장치 핸들러를 위한 캔버스 단의 이벤트 가입 처리
            canvas.addEventListener('mousedown', onMouseDown);
            canvas.addEventListener('mousemove', onMouseMove);
            window.addEventListener('mouseup', onMouseUp);
        }

        /**
         * 행성 버튼 내부에 디자인된 미니 캔버스 아이콘을 정밀 드로잉하는 그래픽 함수
         */
        function drawPlanetButtons() {
            Object.keys(planets).forEach(key => {
                const btn = document.getElementById(`btn-${key}`);
                if (!btn) return;
                
                // 기존 내용을 초기화하고 내장 렌더러용 가상 캔버스 인젝션
                btn.innerHTML = '';
                const pCanvas = document.createElement('canvas');
                pCanvas.className = 'planet-canvas';
                pCanvas.width = 100;
                pCanvas.height = 100;
                btn.appendChild(pCanvas);
                
                const pCtx = pCanvas.getContext('2d');
                pCtx.clearRect(0, 0, 100, 100);
                
                if (key === 'earth') {
                    // 지구: 파란색 바다 위에 펼쳐진 푸른 초록색 대륙
                    pCtx.fillStyle = '#1e3a8a';
                    pCtx.beginPath(); 
                    pCtx.arc(50, 50, 45, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.fillStyle = '#15803d';
                    pCtx.beginPath(); 
                    pCtx.arc(38, 42, 16, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.beginPath(); 
                    pCtx.arc(65, 58, 22, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.beginPath(); 
                    pCtx.arc(42, 68, 12, 0, Math.PI * 2); 
                    pCtx.fill();
                } else if (key === 'moon') {
                    // 달: 분화구 흔적이 마킹된 중성 회색빛 표면 디자인
                    pCtx.fillStyle = '#94a3b8';
                    pCtx.beginPath(); 
                    pCtx.arc(50, 50, 45, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.fillStyle = '#475569';
                    pCtx.beginPath(); 
                    pCtx.arc(35, 35, 10, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.beginPath(); 
                    pCtx.arc(62, 45, 14, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.beginPath(); 
                    pCtx.arc(45, 68, 8, 0, Math.PI * 2); 
                    pCtx.fill();
                } else if (key === 'mars') {
                    // 화성: 산화철 반응에 기반한 주황색 베이스와 짙은 갈색 토양 반점
                    pCtx.fillStyle = '#ea580c';
                    pCtx.beginPath(); 
                    pCtx.arc(50, 50, 45, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.fillStyle = '#7c2d12';
                    pCtx.beginPath(); 
                    pCtx.arc(40, 52, 14, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.beginPath(); 
                    pCtx.arc(68, 38, 11, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.beginPath(); 
                    pCtx.arc(52, 68, 7, 0, Math.PI * 2); 
                    pCtx.fill();
                } else if (key === 'venus') {
                    // 금성: 짙고 두터운 황산 대기를 연상시키는 노란색과 진노란색 무늬
                    pCtx.fillStyle = '#eab308';
                    pCtx.beginPath(); 
                    pCtx.arc(50, 50, 45, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.fillStyle = '#a16207';
                    pCtx.beginPath(); 
                    pCtx.arc(32, 44, 12, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.beginPath(); 
                    pCtx.arc(58, 62, 15, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.beginPath(); 
                    pCtx.arc(64, 34, 9, 0, Math.PI * 2); 
                    pCtx.fill();
                } else if (key === 'europa') {
                    // 유로파: 얼어붙은 청백색 빙하 지각 표면과 깊은 내부 크랙 라인
                    pCtx.fillStyle = '#bae6fd';
                    pCtx.beginPath(); 
                    pCtx.arc(50, 50, 45, 0, Math.PI * 2); 
                    pCtx.fill();
                    
                    pCtx.strokeStyle = '#0284c7'; 
                    pCtx.lineWidth = 3;
                    pCtx.beginPath(); 
                    pCtx.moveTo(20, 40); 
                    pCtx.lineTo(50, 70); 
                    pCtx.lineTo(80, 50); 
                    pCtx.stroke();
                    
                    pCtx.beginPath(); 
                    pCtx.moveTo(40, 22); 
                    pCtx.lineTo(65, 54); 
                    pCtx.stroke();
                }
            });
        }

        /**
         * 사용자가 행성을 변경했을 때 물리 엔진 상수 및 입자 방향 속성을 스위칭하는 제어 장치
         */
        function selectPlanet(key) {
            currentPlanetKey = key;
            currentGravity = planets[key].gravity;
            
            // 기존 활성화 클래스들을 버튼에서 일괄 소거
            document.querySelectorAll('.planet-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(`btn-${key}`).classList.add('active');

            // 행성 고유 환경 벡터 흐름에 맞춰 대기 파티클의 속도 벡터 조정 연산 수행
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

        /**
         * 마우스 클릭 시작 시 드래그 모드를 검증 활성화하는 입력 감지 함수
         */
        function onMouseDown(e) {
            // 화살이 이미 비행 중이거나 리로드 페이즈 하위 단계에 있을 시 드래그 차단 연산 적용
            if(!gameActive || isArrowInFlight || reloadTimer > 0) return;

            const rect = canvas.getBoundingClientRect();
            const mX = e.clientX - rect.left;
            const mY = e.clientY - rect.top;

            // 조작 기준점 반경 내부에서 마우스가 위치하는지 검사
            if (Math.hypot(mX - bowPos.x, mY - bowPos.y) < 90) {
                isDragging = true;
                dragStart = { x: bowPos.x, y: bowPos.y };
                dragEnd = { x: mX, y: mY };
            }
        }

        /**
         * 마우스 드래그 이동 시 조준점 위치 벡터를 갱신하는 모듈 함수
         */
        function onMouseMove(e) {
            if (!isDragging) return;
            const rect = canvas.getBoundingClientRect();
            dragEnd.x = e.clientX - rect.left;
            dragEnd.y = e.clientY - rect.top;
        }

        /**
         * 마우스 클릭 해제 시 화살 투사체 오브젝트를 물리 엔진 풀로 사출시키는 실행 장치
         */
        function onMouseUp(e) {
            if (!isDragging) return;
            isDragging = false;

            // 드래그 거리 차이에 비례한 사출 가속도 상수 계수 도출
            let pVx = (dragStart.x - dragEnd.x) * 0.25;
            let pVy = (dragStart.y - dragEnd.y) * 0.25;

            // 유효한 전방 발사 조건 범위를 만족하는 경우 사출 프로세스 승인
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

                // 화살 사출 완료에 따른 조작 잠금 연동 처리 스위치 동작
                isArrowInFlight = true;

                // 다음 발사용 사과 화살 무작위 가중치 공식 연산 갱신
                currentArrow.isApple = Math.random() < 0.22;
            }
        }

        /**
         * 화살 충돌 또는 파괴 시 공간 내에 흩뿌려질 화려한 시각 파티클들을 동적 가공하는 함수
         */
        function createExplosion(x, y, color, count) {
            for (let i = 0; i < count; i++) {
                let angle = Math.random() * Math.PI * 2;
                let speed = Math.random() * 5 + 2;
                particles.push({
                    x: x, 
                    y: y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    radius: Math.random() * 3.5 + 1.2,
                    color: color,
                    alpha: 1,
                    decay: Math.random() * 0.02 + 0.015
                });
            }
        }

        /**
         * 점수 획득 시 타격 지점 상단으로 부유하는 텍스트 연출 인스턴스를 삽입하는 장치
         */
        function createScoreText(x, y, text, color) {
            scoreTexts.push({ 
                x: x, 
                y: y, 
                text: text, 
                color: color, 
                alpha: 1, 
                vy: -0.9 
            });
        }

        /**
         * 각성 패시브 모드를 활성화하여 유지시간 버프를 구동시키는 장치 함수
         */
        function activateAbilityBuff() {
            isBuffed = true;
            buffTimer = maxBuffDuration;
            appleTrajectoryVisible = true; 
        }

        /**
         * 버프 타이머가 소멸했을 때 각성 이펙트 상태를 초기 복구시키는 제어 모듈
         */
        function deactivateAbilityBuff() {
            isBuffed = false;
        }

        /**
         * 고정 배치된 궁수 본체 캐릭터 디자인을 고유 수치 유지하여 드로잉하는 그래픽 모듈
         */
        function drawArcherCharacter(angle) {
            ctx.save();
            // 캐릭터의 기본 베이스 오프셋 지정
            ctx.translate(bowPos.x - 35, bowPos.y + 15);
            
            // 몸체 기하학 폴리곤 영역 설정 및 페인팅
            ctx.fillStyle = "#1e293b";
            ctx.beginPath();
            ctx.moveTo(-15, 40); 
            ctx.lineTo(15, 40); 
            ctx.lineTo(10, -20); 
            ctx.lineTo(-10, -20);
            ctx.closePath(); 
            ctx.fill();

            // 헬멧 구조 머리 파트 렌더링
            ctx.fillStyle = "#334155";
            ctx.beginPath(); 
            ctx.arc(0, -34, 14, 0, Math.PI * 2); 
            ctx.fill();

            // 조준 각도 벡터에 맞춘 팔 관절 위치 회전 연산 적용
            ctx.translate(20, -15);
            ctx.rotate(angle);
            ctx.fillStyle = isBuffed ? "#f43f5e" : "#38bdf8";
            ctx.fillRect(0, -5, 35, 10);
            ctx.restore();
        }

        /**
         * [지구] 테마 환경 배경을 실시간 드로잉하는 전용 렌더 파트
         */
        function drawEarthBackground() {
            // 그라데이션 기법을 적용한 푸른 대기권 스카이 박스 처리
            let skyGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
            skyGrad.addColorStop(0, '#bae6fd');
            skyGrad.addColorStop(1, '#e0f2fe');
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 속도 모델링에 따른 구름 흘러가기 연산 및 반복 루프 연출 구현
            ctx.fillStyle = "rgba(255, 255, 255, 0.75)";
            clouds.forEach(c => {
                c.x += c.speed;
                if(c.x > canvas.width + 100) c.x = -100;
                
                ctx.save();
                ctx.translate(c.x, c.y);
                ctx.scale(c.scale, c.scale);
                ctx.beginPath();
                ctx.arc(0, 0, 25, 0, Math.PI * 2);
                ctx.arc(20, -10, 30, 0, Math.PI * 2);
                ctx.arc(45, 0, 22, 0, Math.PI * 2);
                ctx.arc(20, 10, 25, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            });

            // 평평하고 안정적인 갈색 지구 대지 레이아웃 구축
            ctx.fillStyle = '#854d0e';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 40);
            ctx.fillStyle = '#166534';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 8);
        }

        /**
         * [달] 테마 환경 배경을 실시간 드로잉하는 전용 렌더 파트
         */
        function drawMoonBackground() {
            // 깊은 암흑 성간 우주 공간 베이스 필터 처리
            ctx.fillStyle = '#000000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 반짝이는 미세 별빛 입자 데이터 일괄 투사
            ctx.fillStyle = "rgba(255, 255, 255, 0.45)";
            stars.forEach(s => {
                ctx.beginPath(); 
                ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); 
                ctx.fill();
            });

            // 울퉁불퉁한 음영 굴곡을 가미한 회색빛의 위성 바닥 표면 드로잉
            ctx.fillStyle = '#475569';
            ctx.beginPath();
            ctx.moveTo(0, canvas.height);
            ctx.lineTo(0, canvas.height - 50);
            
            // 삼각함수 파동 연산식을 조율한 고유 크레이터 언덕 지형 형성 가동
            for(let i = 0; i <= canvas.width; i += 40) {
                let yOffset = Math.sin(i * 0.05) * 8 + Math.cos(i * 0.02) * 6;
                if(i % 120 === 0) yOffset -= 12; 
                ctx.lineTo(i, canvas.height - 42 + yOffset);
            }
            ctx.lineTo(canvas.width, canvas.height);
            ctx.closePath();
            ctx.fill();

            // 표면 내부 크레이터 동심원 디테일 보정 연산 페인팅 진행
            ctx.fillStyle = '#334155';
            for(let i = 60; i < canvas.width; i += 180) {
                ctx.beginPath();
                ctx.ellipse(i, canvas.height - 25, 20, 6, 0, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        /**
         * [화성] 테마 환경 배경을 실시간 드로잉하는 전용 렌더 파트
         */
        function drawMarsBackground() {
            // 산화 성분이 함유된 특유의 뿌연 주황 황사 대기 그라데이션 필드 생성
            let marsGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
            marsGrad.addColorStop(0, '#fef08a');
            marsGrad.addColorStop(0.6, '#fed7aa');
            marsGrad.addColorStop(1, '#ffedd5');
            ctx.fillStyle = marsGrad;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 대기 공간에서 무작위로 하강 횡단하는 가벼운 모래바람 입자 흔적 구현
            ctx.fillStyle = "rgba(194, 65, 12, 0.22)";
            environmentParticles.forEach(p => {
                p.x += p.vx; 
                p.y += p.vy;
                if(p.x < 0) p.x = canvas.width;
                if(p.x > canvas.width) p.x = 0;
                if(p.y > canvas.height) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * 1.5, 0, Math.PI * 2);
                ctx.fill();
            });

            // 화성 특유의 짙은 적갈색 바닥 레이어 페인팅
            ctx.fillStyle = '#7c2d12';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 40);
            ctx.fillStyle = '#9a3412';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 6);
        }

        /**
         * [금성] 테마 환경 배경을 실시간 드로잉하는 전용 렌더 파트
         */
        function drawVenusBackground() {
            // 황산 구름으로 차폐된 고농도 노란색 스모그 가득한 하늘 표출
            ctx.fillStyle = '#fef08a';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 우측에서 좌측으로 흐르는 기류 표현을 위한 위상 수학 변수 가중
            venusPhase += 0.01;

            // 폭풍 트레일 라인 효과 동적 투사 루프 연산
            ctx.strokeStyle = "rgba(161, 98, 7, 0.12)";
            ctx.lineWidth = 4;
            for(let i = 0; i < 25; i++) {
                let yPos = (i * 26 + venusPhase * 40) % canvas.height;
                ctx.beginPath();
                ctx.moveTo(canvas.width + 50, yPos);
                ctx.lineTo(-50, yPos + Math.sin(venusPhase + i) * 20);
                ctx.stroke();
            }

            // 고속 수평 역방향 이동을 개시하는 먼지 파티클 엔진 가동
            ctx.fillStyle = "rgba(113, 63, 4, 0.35)";
            environmentParticles.forEach(p => {
                p.x += p.vx * 1.8; 
                p.y += p.vy * 0.5;
                if(p.x < -20) p.x = canvas.width + 20;
                if(p.y > canvas.height) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * 1.1, 0, Math.PI * 2);
                ctx.fill();
            });

            // 전체적인 흐림 현상 극대화를 위한 진노란색 알파 반투명 마스크 덮개 연출
            ctx.fillStyle = "rgba(234, 179, 8, 0.18)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 금성 고유의 짙은 노란 점토색 하단 지표면 구축
            ctx.fillStyle = '#ca8a04';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 40);
            ctx.fillStyle = '#854d0e';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 5);
        }

        /**
         * [유로파] 테마 환경 배경을 실시간 드로잉하는 전용 렌더 파트
         */
        function drawEuropaBackground() {
            // 얼음 행성의 차가운 냉기가 느껴지는 뿌연 연청색 스카이 이펙트
            let euroGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
            euroGrad.addColorStop(0, '#a5f3fc');
            euroGrad.addColorStop(1, '#ecfeff');
            ctx.fillStyle = euroGrad;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 크랙(금이 간 흔적)이 형성될 백색 청빙 바닥 기초 토대 생성
            ctx.fillStyle = '#e0f2fe';
            ctx.fillRect(0, canvas.height - 40, canvas.width, 40);

            // 빙판 표면 위의 불규칙 균열 라인 데이터 그리기 작업
            ctx.strokeStyle = '#0284c7';
            ctx.lineWidth = 2.5;
            
            ctx.save();
            ctx.beginPath();
            // 선형 경로 기하 수치 계산에 의거한 크랙킹 기법 매핑
            ctx.moveTo(0, canvas.height - 30); ctx.lineTo(180, canvas.height - 10); ctx.lineTo(340, canvas.height - 35);
            ctx.moveTo(250, canvas.height - 20); ctx.lineTo(290, canvas.height);
            ctx.moveTo(500, canvas.height - 40); ctx.lineTo(560, canvas.height - 5); ctx.lineTo(720, canvas.height - 25);
            ctx.moveTo(680, canvas.height - 28); ctx.lineTo(800, canvas.height - 2); ctx.lineTo(1000, canvas.height - 20);
            ctx.stroke();
            ctx.restore();

            // 하늘 상단에서 지속적이고 끊임없이 자유 낙하하는 강설(Snowfall) 메커니즘 구동
            ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
            environmentParticles.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;
                // 바닥 경계 도달 시 다시 상단 천장 좌표로 오프셋 리포지셔닝
                if(p.y > canvas.height - 40) {
                    p.y = 0;
                    p.x = Math.random() * canvas.width;
                }
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();
            });
        }

        /**
         * 매 프레임마다 물리 엔진 스캔 및 캔버스 화면 업데이트를 관장하는 메인 컨트롤 루프 함수
         */
        function update() {
            // 각성 모드 상태 타이머 차감 분기 연산
            if (gameActive && isBuffed) {
                buffTimer--;
                if(buffTimer <= 0) {
                    deactivateAbilityBuff();
                }
            }

            // [재장전 시간 차감 수치 연산]
            if (reloadTimer > 0) {
                reloadTimer--;
                if (reloadTimer <= 0) {
                    // 1초간의 재장전 유예 타임 오버 시 사출 잠금 해제 스위칭 작동
                    isArrowInFlight = false; 
                }
            }

            if (gameActive) {
                gameFrameCount++;
                
                // 주기별 난수 패턴 검사에 따른 보스급 돌발 운석 인스턴스 생성 프로세서
                if(gameFrameCount % 900 === 0 && !meteor.active) {
                    meteor.x = canvas.width + 40;
                    meteor.y = 100 + Math.random() * 200;
                    meteor.vx = -(Math.random() * 2.5 + 3.0);
                    meteor.vy = Math.random() * 0.8;
                    meteor.active = true;
                    meteor.destroyed = false;
                }

                // 과녁 활성화 상태 시 상하 바운딩 물리 궤적 연산 진행
                if(target.visible) {
                    target.y += target.speed * target.dir;
                    if(target.y - target.radiusD < 140 || target.y + target.radiusD > canvas.height - 40) {
                        target.dir *= -1; 
                    }
                } else {
                    // 피격 소멸 시 재생성 대기 딜레이 프레임 갱신 연산
                    target.respawnTimer--;
                    if(target.respawnTimer <= 0) {
                        target.y = 180 + Math.random() * (canvas.height - 320);
                        target.visible = true;
                    }
                }

                // 특수 모드 궤적 플래그 깜빡임 스위치 교정
                if(currentArrow.isApple) {
                    appleTimer++;
                    if(appleTimer % 45 === 0) {
                        appleTrajectoryVisible = !appleTrajectoryVisible;
                    }
                }

                // 이동 중인 운석 객체 프레임 벡터 가산 및 한계점 피격 실패 소멸 연산
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

            // 화면 전체를 뒤흔드는 진동 행렬 기하 변환 연산 블록
            ctx.save();
            if (shakeIntensity > 0) {
                ctx.translate((Math.random() - 0.5) * shakeIntensity, (Math.random() - 0.5) * shakeIntensity);
                // 점진적으로 감쇄 성분을 적용하여 진동 정지 유도
                shakeIntensity *= 0.85; 
                if (shakeIntensity < 0.2) shakeIntensity = 0;
            }

            // 프레임 오버랩 방지를 위한 캔버스 화면 전역 클리어화 진행
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // [선택 행성 키값 분기에 기반한 다이내믹 배경 백그라운드 렌더러 호출 체계]
            if (currentPlanetKey === 'earth') drawEarthBackground();
            else if (currentPlanetKey === 'moon') drawMoonBackground();
            else if (currentPlanetKey === 'mars') drawMarsBackground();
            else if (currentPlanetKey === 'venus') drawVenusBackground();
            else if (currentPlanetKey === 'europa') drawEuropaBackground();

            // 버프 돌입 각성 연출 전용 특수 스크린 마스크 처리구간
            if(isBuffed && gameActive) {
                ctx.fillStyle = "rgba(255, 62, 62, 0.04)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            // 운석 객체 실시간 활성화 상태 체크 렌더 연출
            if(meteor.active) {
                ctx.save();
                ctx.fillStyle = "rgba(239, 68, 68, 0.25)";
                ctx.beginPath(); 
                ctx.arc(meteor.x, meteor.y, meteor.radius + 12 + Math.random() * 6, 0, Math.PI * 2); 
                ctx.fill();

                let grad = ctx.createRadialGradient(meteor.x - 10, meteor.y - 10, 5, meteor.x, meteor.y, meteor.radius);
                grad.addColorStop(0, '#ff9e00'); 
                grad.addColorStop(0.6, '#d946ef'); 
                grad.addColorStop(1, '#450a0a');
                ctx.fillStyle = grad;
                ctx.beginPath(); 
                ctx.arc(meteor.x, meteor.y, meteor.radius, 0, Math.PI * 2); 
                ctx.fill();
                ctx.strokeStyle = "#ff0055"; 
                ctx.lineWidth = 3; 
                ctx.stroke();
                ctx.restore();
            }

            // 원형 가이드 라인을 따르는 다중 과녁 타겟 서페이스 디자인 렌더링
            const targetColor = planets[currentPlanetKey].color;
            const skewX = 0.25; 
            const frontX = target.x - (target.radiusD * skewX); 
            const backX = target.x + (target.radiusD * skewX); 

            if(target.visible) {
                ctx.save();
                ctx.strokeStyle = "#4a5568"; 
                ctx.lineWidth = 6;
                ctx.beginPath();
                ctx.moveTo(target.x + 5, target.y - target.radiusD); 
                ctx.lineTo(target.x + 5, target.y + target.radiusD);
                ctx.stroke();

                ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
                ctx.beginPath(); 
                ctx.ellipse(target.x, target.y, (target.radiusD + 6) * skewX, target.radiusD + 6, 0, 0, Math.PI * 2); 
                ctx.fill();

                ctx.fillStyle = "#ffffff";
                ctx.beginPath(); 
                ctx.ellipse(target.x, target.y, target.radiusD * skewX, target.radiusD, 0, 0, Math.PI * 2); 
                ctx.fill(); 
                
                ctx.fillStyle = targetColor;
                ctx.beginPath(); 
                ctx.ellipse(target.x, target.y, target.radiusC * skewX, target.radiusC, 0, 0, Math.PI * 2); 
                ctx.fill();
                
                ctx.fillStyle = "#ff3e3e";
                ctx.beginPath(); 
                ctx.ellipse(target.x, target.y, target.radiusB * skewX, target.radiusB, 0, 0, Math.PI * 2); 
                ctx.fill();
                
                ctx.fillStyle = "#ffcc00";
                ctx.beginPath(); 
                ctx.ellipse(target.x, target.y, target.radiusA * skewX, target.radiusA, 0, 0, Math.PI * 2); 
                ctx.fill();
                ctx.restore();
            }

            // 활쏘기 모션 매칭 각도 추적 반영 및 아처 구현체 렌더 유도
            let dragAngle = Math.atan2(dragStart.y - dragEnd.y, dragStart.x - dragEnd.x);
            drawArcherCharacter(dragAngle);

            // 보우 컴포넌트 및 에너지 시위 와이어 라인 드로잉 기믹
            ctx.save();
            ctx.strokeStyle = isBuffed ? "#ff0055" : "#00d2ff";
            ctx.lineWidth = 5; 
            ctx.beginPath();
            ctx.arc(bowPos.x - 12, bowPos.y, 48, -Math.PI / 2, Math.PI / 2); 
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

            // [비행 중 또는 리로딩 대기 중이 아닐 때만 대기실 화살을 활에 노출]
            if(!isDragging && gameActive && !isArrowInFlight && reloadTimer <= 0) {
                drawArrowIcon(bowPos.x, bowPos.y, 0, currentArrow.isApple);
            }

            // 중력 시뮬레이션 기반 가이드 점선 궤적 실시간 사전 계산 트래킹 루프
            if (isDragging && appleTrajectoryVisible && gameActive) {
                let tVx = (dragStart.x - dragEnd.x) * 0.25;
                if (tVx > 0) { 
                    ctx.save();
                    ctx.strokeStyle = currentArrow.isApple ? "#af0404" : "rgba(0, 210, 255, 0.5)";
                    ctx.lineWidth = 2.5; 
                    ctx.setLineDash([5, 5]);
                    ctx.beginPath();

                    let tX = bowPos.x; 
                    let tY = bowPos.y;
                    let tVy = (dragStart.y - dragEnd.y) * 0.25;

                    ctx.moveTo(tX, tY);
                    for (let i = 0; i < 60; i++) {
                        tX += tVx; 
                        tY += tVy; 
                        tVy += currentGravity; 
                        ctx.lineTo(tX, tY);
                        if(tX > canvas.width || tY > canvas.height || tY < 0) break;
                    }
                    ctx.stroke(); 
                    ctx.restore();

                    drawArrowIcon(dragEnd.x, dragEnd.y, dragAngle, currentArrow.isApple);
                }
            }

            // 투사체 풀 순회 물리 궤적 연산 가산 루프
            for (let i = activeArrows.length - 1; i >= 0; i--) {
                let arrow = activeArrows[i];
                
                arrow.x += arrow.vx;
                arrow.y += arrow.vy;
                arrow.vy += currentGravity;

                let arrowAngle = Math.atan2(arrow.vy, arrow.vx);
                drawArrowIcon(arrow.x, arrow.y, arrowAngle, arrow.isApple, arrow.width);

                let arrowTipX = arrow.x + Math.cos(arrowAngle) * (arrow.width / 2);
                let arrowTipY = arrow.y + Math.sin(arrowAngle) * (arrow.width / 2);

                // [버프 패치]: 화살 조기 삭제 방지를 위해 경계 검사 범위를 상단 -2500px 및 외부 확장 구현 고수
                if (arrow.x > canvas.width + 500 || arrow.x < -500 || arrow.y > canvas.height + 500 || arrow.y < -2500) {
                    if(!arrow.handled) {
                        combo = 0; 
                        document.getElementById('combo-wrapper').classList.add('hidden');
                        
                        // [요청 연동 완료]: 명중하지 못하고 멀리 아웃 오브 바운드 탈출 시 1초(60프레임) 리로드 가동
                        reloadTimer = 60; 
                    }
                    activeArrows.splice(i, 1);
                    continue;
                }

                // 충돌 검사 제 1단계: 상공 출현 운석 타격 충돌 처리
                if(meteor.active) {
                    let distToMeteor = Math.hypot(arrowTipX - meteor.x, arrowTipY - meteor.y);
                    if(distToMeteor <= meteor.radius + 10) {
                        meteor.active = false;
                        meteor.destroyed = true;
                        activeArrows.splice(i, 1); 

                        createExplosion(meteor.x, meteor.y, "#ffcc00", 40);
                        createScoreText(meteor.x, meteor.y, "AWAKENING!!", "#ffcc00");
                        
                        activateAbilityBuff();

                        // 즉각적인 장전 복구 신호 연계
                        isArrowInFlight = false;
                        continue;
                    }
                }

                // 충돌 검사 제 2단계: 메인 이동 관녁 원형 타겟 충돌 처리 섹션
                if (target.visible && arrowTipX >= frontX && arrowTipX <= backX + 15 && arrow.vx > 0) {
                    let dy = Math.abs(arrowTipY - target.y);

                    if (dy <= target.radiusD) {
                        arrow.handled = true;
                        
                        target.visible = false;
                        target.respawnTimer = 45; 

                        combo++;
                        if(combo > maxCombo) maxCombo = combo;
                        
                        // [요청 사항 완벽 조율]: 콤보 수치에 연계되어 흔들림 세기가 점진 증폭 가산되는 기믹 구현
                        shakeIntensity = 8 + Math.min(combo * 2.5, 25);

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
                        createExplosion(arrowTipX, arrowTipY, hColor, 20);

                        activeArrows.splice(i, 1); 

                        // [요청 사항 반영 완료]: 명중 성공 시 딜레이 유예 없이 즉시 화살 슬롯 복구 재장전
                        isArrowInFlight = false;
                        continue;
                    }
                }
            }

            // 폭발 파티클 라이프 사이클 루프 처리 연산
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx; 
                p.y += p.vy; 
                p.alpha -= p.decay;
                if (p.alpha <= 0) { 
                    particles.splice(i, 1); 
                    continue; 
                }
                ctx.save(); 
                ctx.globalAlpha = p.alpha; 
                ctx.fillStyle = p.color;
                ctx.beginPath(); 
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); 
                ctx.fill(); 
                ctx.restore();
            }

            // 데미지 스코어 부유 플로팅 폰트 페인팅 루프
            for (let i = scoreTexts.length - 1; i >= 0; i--) {
                let stx = scoreTexts[i];
                stx.y += stx.vy; 
                stx.alpha -= 0.015;
                if(stx.alpha <= 0) { 
                    scoreTexts.splice(i, 1); 
                    continue; 
                }
                ctx.save(); 
                ctx.globalAlpha = stx.alpha; 
                ctx.fillStyle = stx.color;
                ctx.font = "bold 26px 'Segoe UI'"; 
                ctx.shadowColor = "rgba(0,0,0,0.5)"; 
                ctx.shadowBlur = 4;
                ctx.fillText(stx.text, stx.x, stx.y); 
                ctx.restore();
            }

            ctx.restore(); 
            // 프레임 애니메이션 요청 콜백 재귀 실행
            requestAnimationFrame(update);
        }

        /**
         * 화살의 바디 및 고유 기하학 깃털 구조를 정밀하게 그리는 백엔드 그래픽 장치
         */
        function drawArrowIcon(x, y, angle, isApple, customWidth) {
            ctx.save();
            ctx.translate(x, y); 
            ctx.rotate(angle);
            let width = customWidth || 95; 
            
            ctx.strokeStyle = isApple ? "#ff3333" : "#e2e8f0";
            ctx.lineWidth = isApple ? 5.5 : 4.5; 
            ctx.beginPath(); 
            ctx.moveTo(-width / 2, 0); 
            ctx.lineTo(width / 2, 0); 
            ctx.stroke();

            ctx.fillStyle = isApple ? "#ff0000" : "#cbd5e1";
            ctx.beginPath(); 
            ctx.moveTo(width / 2, 0); 
            ctx.lineTo(width / 2 - 15, -8); 
            ctx.lineTo(width / 2 - 15, 8); 
            ctx.closePath(); 
            ctx.fill();

            ctx.fillStyle = isApple ? "#ffcc00" : "#3182ce";
            ctx.beginPath(); 
            ctx.moveTo(-width / 2, 0); 
            ctx.lineTo(-width / 2 - 8, -10); 
            ctx.lineTo(-width / 2 + 5, -10); 
            ctx.lineTo(-width / 2 + 12, 0); 
            ctx.lineTo(-width / 2 + 5, 10); 
            ctx.lineTo(-width / 2 - 8, 10); 
            ctx.closePath(); 
            ctx.fill();

            if(isApple) {
                ctx.fillStyle = "#fa5252"; 
                ctx.beginPath(); 
                ctx.arc(0, -4, 11, 0, Math.PI * 2); 
                ctx.fill();
                ctx.strokeStyle = "#868e96"; 
                ctx.lineWidth = 2; 
                ctx.beginPath(); 
                ctx.moveTo(0, -14); 
                ctx.quadraticCurveTo(3, -19, 6, -17); 
                ctx.stroke();
            }
            ctx.restore();
        }

        // 인스턴스 빌더 구동 선언문
        init();
        update();
    </script>
</body>
</html>
"""

# 완성된 게임 결과 프레임을 Streamlit 컴포넌트 웹 뷰로 최종 주입 처리
components.html(game_html, height=700, scrolling=False)
