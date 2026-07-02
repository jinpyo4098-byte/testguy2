import streamlit as st

# Set up page configuration
st.set_page_config(
    page_title="Gravity Arrow - Physics Simulation Game",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Render main Streamlit titles and description
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 10px;">
        <h1 style="color: #1E3A8A; font-family: 'Arial Black', sans-serif; font-size: 2.8rem; margin-bottom: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
            🎯 Gravity Arrow (그래비티 애로우)
        </h1>
        <p style="color: #4B5563; font-size: 1.1rem; font-weight: 500;">
            고등학교 물리학 및 지구과학 융합 프로젝트: 천체별 중력과 대기 저항 환경에서의 포물선 운동 시뮬레이션 게임
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Entire Game Implementation within a single robust HTML5 Canvas & JS Container
game_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Gravity Arrow</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f3f4f6;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            user-select: none;
        }

        /* Top Dashboard Control Panel */
        .control-panel {
            width: 850px;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 15px 20px;
            margin-bottom: 15px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.5);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .panel-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Planet Selection Buttons */
        .planet-group {
            display: flex;
            gap: 8px;
        }

        .planet-btn {
            padding: 8px 14px;
            font-size: 0.9rem;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            color: #ffffff;
        }

        .btn-earth   { background-color: #3b82f6; }
        .btn-moon    { background-color: #6b7280; }
        .btn-mars    { background-color: #ea580c; }
        .btn-venus   { background-color: #ca8a04; }
        .btn-europa  { background-color: #06b6d4; }

        .planet-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            filter: brightness(1.1);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }

        .planet-btn.active {
            ring: 3px solid #000;
            outline: 3px solid #1f2937;
            transform: scale(1.05);
        }

        .planet-btn:disabled {
            background-color: #d1d5db !important;
            color: #9ca3af !important;
            cursor: not-allowed;
            transform: none !important;
            box-shadow: none !important;
        }

        /* Start Button */
        .start-btn {
            padding: 10px 24px;
            font-size: 1.1rem;
            font-weight: 700;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2);
        }

        .start-btn:hover:not(:disabled) {
            transform: translateY(-1px);
            box-shadow: 0 6px 12px rgba(16, 185, 129, 0.3);
            filter: brightness(1.05);
        }
        
        .start-btn:disabled {
            background: #9ca3af;
            cursor: not-allowed;
            box-shadow: none;
        }

        /* Score & Stats display */
        .score-container {
            display: flex;
            gap: 20px;
            font-size: 1.1rem;
            font-weight: 700;
            color: #1f2937;
        }

        .high-score {
            color: #b91c1c;
            background: #fee2e2;
            padding: 4px 10px;
            border-radius: 6px;
        }

        /* HUD Stats Bar */
        .hud-bar {
            display: flex;
            justify-content: space-between;
            background: #1f2937;
            color: #ffffff;
            border-radius: 10px;
            padding: 8px 15px;
            font-size: 0.9rem;
            font-family: monospace;
        }

        .hud-item span {
            color: #38bdf8;
            font-weight: bold;
        }

        /* Canvas Game Viewport */
        #gameCanvas {
            background-color: #ffffff;
            border-radius: 16px;
            box-shadow: 0 20px 4px -5px rgba(0,0,0,0.02), 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            cursor: crosshair;
        }
    </style>
</head>
<body>

    <div class="control-panel">
        <div class="panel-row">
            <div class="planet-group" id="planetGroup">
                <button class="planet-btn btn-earth active" onclick="selectPlanet('earth')">지구 (Earth)</button>
                <button class="planet-btn btn-moon" onclick="selectPlanet('moon')">달 (Moon)</button>
                <button class="planet-btn btn-mars" onclick="selectPlanet('mars')">화성 (Mars)</button>
                <button class="planet-btn btn-venus" onclick="selectPlanet('venus')">금성 (Venus)</button>
                <button class="planet-btn btn-europa" onclick="selectPlanet('europa')">유로파 (Europa)</button>
            </div>
            
            <button class="start-btn" id="startBtn" onclick="startGame()">공격 개시 (Start)</button>

            <div class="score-container">
                <div>현재 점수: <span id="currentScore">0</span></div>
                <div class="high-score">최고 기록: <span id="highScoreDisplay">0</span></div>
            </div>
        </div>

        <div class="hud-bar">
            <div class="hud-item">천체명: <span id="hudPlanet">지구 (Earth)</span></div>
            <div class="hud-item">중력 가속도: <span id="hudGravity">9.8 m/s²</span></div>
            <div class="hud-item">환경 변수(풍속): <span id="hudWind">0.0 m/s</span></div>
            <div class="hud-item" style="font-size: 1.05rem;">남은 시간: <span id="hudTimer" style="color: #f43f5e;">15.00s</span></div>
        </div>
    </div>

    <canvas id="gameCanvas" width="850" height="500"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // Environmental Settings Mapping
        const environments = {
            earth: { name: "지구 (Earth)", gravity: 9.8, windMin: -2.0, windMax: 2.0 },
            moon: { name: "달 (Moon)", gravity: 1.6, windMin: 0.0, windMax: 0.0 },
            mars: { name: "화성 (Mars)", gravity: 3.7, windMin: -1.0, windMax: 1.0 },
            venus: { name: "금성 (Venus)", gravity: 8.9, windMin: -4.0, windMax: 4.0 },
            europa: { name: "유로파 (Europa)", gravity: 1.3, windMin: -0.5, windMax: 0.5 }
        };

        // Game State Variables
        let currentPlanetKey = 'earth';
        let isPlaying = false;
        let score = 0;
        let highScore = localStorage.getItem('gravityArrow_highScore') || 0;
        let timeLeft = 15.00;
        let currentWind = 0;
        let lastTime = 0;

        // Physics Entities
        const bow = { x: 120, y: 320, radius: 45 };
        let arrows = [];
        let activeArrow = null; // Currently queued arrow for launching
        let target = {
            x: 750,
            y: 200,
            vy: 2.5,
            radiusD: 40,
            radiusC: 30,
            radiusB: 20,
            radiusA: 10,
            directionTimer: 0,
            respawnTimer: 0,
            isDead: false
        };

        // Interaction State
        let drag = {
            isDragging: false,
            startX: 0,
            startY: 0,
            currentX: 0,
            currentY: 0
        };

        // Juice Effects
        let screenShakeTime = 0;
        let targetParticles = [];
        let trajectoryShakeTimer = 0;
        let trajectoryShakeOffset = { x: 0, y: 0 };

        // Initialize highscore view
        document.getElementById('highScoreDisplay').innerText = highScore;

        // Soundless procedural graphics helper for planetary backgrounds
        function rand(min, max) { return Math.random() * (max - min) + min; }

        // Setup environment parameters
        function initEnvironment() {
            const env = environments[currentPlanetKey];
            document.getElementById('hudPlanet').innerText = env.name;
            document.getElementById('hudGravity').innerText = env.gravity.toFixed(1) + " m/s²";
            
            // Randomize wind based on planet boundaries
            currentWind = rand(env.windMin, env.windMax);
            document.getElementById('hudWind').innerText = (currentWind >= 0 ? "+" : "") + currentWind.toFixed(1) + " m/s";
            
            // Reset entities
            arrows = [];
            spawnNewArrow();
        }

        function selectPlanet(planetKey) {
            if (isPlaying) return;
            currentPlanetKey = planetKey;
            
            // Toggle active visual class
            const buttons = document.querySelectorAll('.planet-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            initEnvironment();
        }

        function spawnNewArrow() {
            // 5% chance to obtain Apple Arrow
            const isApple = Math.random() < 0.05;
            activeArrow = {
                x: bow.x,
                y: bow.y,
                vx: 0,
                vy: 0,
                launched: false,
                isApple: isApple,
                angle: 0,
                length: 50
            };
        }

        function startGame() {
            if (isPlaying) return;
            
            isPlaying = true;
            score = 0;
            timeLeft = 15.00;
            document.getElementById('currentScore').innerText = score;
            
            // Lock UI elements
            document.getElementById('startBtn').disabled = true;
            const buttons = document.querySelectorAll('.planet-btn');
            buttons.forEach(btn => btn.disabled = true);

            // Re-roll environmental wind vector upon game kickoff
            initEnvironment();
            
            // Reset target position
            target.y = 200;
            target.vy = environments[currentPlanetKey].gravity > 5 ? 3 : 1.8; 
            target.directionTimer = 0;
            target.isDead = false;
            target.respawnTimer = 0;
            
            lastTime = performance.now();
            requestAnimationFrame(gameLoop);
        }

        function endGame() {
            isPlaying = false;
            document.getElementById('startBtn').disabled = false;
            const buttons = document.querySelectorAll('.planet-btn');
            buttons.forEach(btn => btn.disabled = false);

            // Update high score records cleanly
            if (score > highScore) {
                highScore = score;
                localStorage.setItem('gravityArrow_highScore', highScore);
                document.getElementById('highScoreDisplay').innerText = highScore;
            }
            alert("게임 종료! 최종 점수: " + score + "점");
        }

        // --- Interaction Event Listeners ---
        canvas.addEventListener('mousedown', (e) => {
            if (!isPlaying || !activeArrow) return;
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            // Check if click is relatively close to the bow installation station
            const dist = Math.hypot(mouseX - bow.x, mouseY - bow.y);
            if (dist < 80) {
                drag.isDragging = true;
                drag.startX = bow.x;
                drag.startY = bow.y;
                drag.currentX = mouseX;
                drag.currentY = mouseY;
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!drag.isDragging) return;
            const rect = canvas.getBoundingClientRect();
            drag.currentX = e.clientX - rect.left;
            drag.currentY = e.clientY - rect.top;
        });

        canvas.addEventListener('mouseup', (e) => {
            if (!drag.isDragging) return;
            drag.isDragging = false;

            // Calculate launch vectors based on string displacement vector
            const dx = drag.startX - drag.currentX;
            const dy = drag.startY - drag.currentY;
            const pullDist = Math.hypot(dx, dy);
            
            if (pullDist > 10) {
                // Apply velocity calculations (Base scale factor optimized for responsive launch feel)
                const baseSpeedScale = 0.28;
                activeArrow.vx = dx * baseSpeedScale;
                activeArrow.vy = dy * baseSpeedScale;
                activeArrow.launched = true;
                
                arrows.push(activeArrow);
                spawnNewArrow(); // Instant Reload mechanic
            }
        });

        // Touch systems overlay compatibility for high school tablet configurations
        canvas.addEventListener('touchstart', (e) => {
            if (e.touches.length === 0) return;
            const t = e.touches[0];
            const rect = canvas.getBoundingClientRect();
            const mouseX = t.clientX - rect.left;
            const mouseY = t.clientY - rect.top;
            const dist = Math.hypot(mouseX - bow.x, mouseY - bow.y);
            if (dist < 80) {
                drag.isDragging = true;
                drag.startX = bow.x;
                drag.startY = bow.y;
                drag.currentX = mouseX;
                drag.currentY = mouseY;
                e.preventDefault();
            }
        });

        canvas.addEventListener('touchmove', (e) => {
            if (!drag.isDragging || e.touches.length === 0) return;
            const t = e.touches[0];
            const rect = canvas.getBoundingClientRect();
            drag.currentX = t.clientX - rect.left;
            drag.currentY = t.clientY - rect.top;
            e.preventDefault();
        });

        canvas.addEventListener('touchend', (e) => {
            if (!drag.isDragging) return;
            drag.isDragging = false;
            const dx = drag.startX - drag.currentX;
            const dy = drag.startY - drag.currentY;
            const pullDist = Math.hypot(dx, dy);
            if (pullDist > 10) {
                const baseSpeedScale = 0.28;
                activeArrow.vx = dx * baseSpeedScale;
                activeArrow.vy = dy * baseSpeedScale;
                activeArrow.launched = true;
                arrows.push(activeArrow);
                spawnNewArrow();
            }
        });


        // --- Core Game Loops & Computational Math Engine ---
        function gameLoop(timestamp) {
            if (!isPlaying) return;

            let dt = (timestamp - lastTime) / 1000;
            if (dt > 0.1) dt = 0.1; // Clamp maximum step size
            lastTime = timestamp;

            timeLeft -= dt;
            if (timeLeft <= 0) {
                timeLeft = 0;
                document.getElementById('hudTimer').innerText = "0.00s";
                render();
                endGame();
                return;
            }
            document.getElementById('hudTimer').innerText = timeLeft.toFixed(2) + "s";

            updatePhysics(dt);
            render();

            requestAnimationFrame(gameLoop);
        }

        function updatePhysics(dt) {
            const env = environments[currentPlanetKey];
            const gPhysics = env.gravity * 2.5; // Scaled mapping to canvas coordinate speeds
            const wPhysics = currentWind * 1.5;

            // Update Trajectory Wobble timers for the unstable Apple Arrow debuff
            trajectoryShakeTimer += dt;
            if (trajectoryShakeTimer >= 1.0) {
                trajectoryShakeTimer = 0;
                trajectoryShakeOffset.x = rand(-15, 15);
                trajectoryShakeOffset.y = rand(-15, 15);
            }

            // Screen shake dampening loop
            if (screenShakeTime > 0) screenShakeTime -= dt;

            // Target AI routine tracking 5-second structural redirection intervals
            if (!target.isDead) {
                target.directionTimer += dt;
                if (target.directionTimer >= 5.0) {
                    target.vy = -target.vy;
                    target.directionTimer = 0;
                }

                target.y += target.vy * (dt * 60);

                // Boundary verification safeguards
                if (target.y - target.radiusD < 20) {
                    target.y = 20 + target.radiusD;
                    target.vy = Math.abs(target.vy);
                } else if (target.y + target.radiusD > 430) {
                    target.y = 430 - target.radiusD;
                    target.vy = -Math.abs(target.vy);
                }
            } else {
                // Handle respawn timer metrics
                target.respawnTimer += dt;
                if (target.respawnTimer >= 1.0) {
                    target.isDead = false;
                    target.y = rand(100, 380);
                    target.directionTimer = 0;
                    target.respawnTimer = 0;
                }
            }

            // Bullet Engine loops checking arrow arrays
            for (let i = arrows.length - 1; i >= 0; i--) {
                let arrow = arrows[i];
                
                // Continuous integration computations
                arrow.vx += wPhysics * dt;
                arrow.vy += gPhysics * dt;
                arrow.x += arrow.vx * (dt * 60);
                arrow.y += arrow.vy * (dt * 60);
                arrow.angle = Math.atan2(arrow.vy, arrow.vx);

                // Collision Detection: Target checks
                if (!target.isDead) {
                    const tipX = arrow.x + Math.cos(arrow.angle) * (arrow.length / 2);
                    const tipY = arrow.y + Math.sin(arrow.angle) * (arrow.length / 2);
                    const distance = Math.hypot(tipX - target.x, tipY - target.y);

                    if (distance <= target.radiusD) {
                        // Scoring logic by sub-concentric radius evaluation
                        let pointsGained = 0;
                        if (distance <= target.radiusA) {
                            pointsGained = 10;
                        } else if (distance <= target.radiusB) {
                            pointsGained = 5;
                        } else if (distance <= target.radiusC) {
                            pointsGained = 2;
                        } else {
                            pointsGained = 1;
                        }

                        // Apply 2x scoring multiplier if Apple Arrow buff is active
                        if (arrow.isApple) pointsGained *= 2;

                        score += pointsGained;
                        document.getElementById('currentScore').innerText = score;

                        // Trigger shatter particle system
                        triggerShatter(target.x, target.y);
                        screenShakeTime = 0.2; // Trigger 0.2-second screen juice warp
                        target.isDead = true;
                        target.respawnTimer = 0;

                        // Remove arrow from tracking
                        arrows.splice(i, 1);
                        continue;
                    }
                }

                // Bounds cleanup cleanup to save render passes
                if (arrow.x > 900 || arrow.x < -100 || arrow.y > 600 || arrow.y < -200) {
                    arrows.splice(i, 1);
                }
            }

            // Update particle explosions physics frame
            for (let i = targetParticles.length - 1; i >= 0; i--) {
                let p = targetParticles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.alpha -= p.fade;
                p.rot += p.rotSpeed;
                if (p.alpha <= 0) {
                    targetParticles.splice(i, 1);
                }
            }
        }

        function triggerShatter(tx, ty) {
            const shardColors = ['#f59e0b', '#ef4444', '#111827', '#ffffff'];
            for (let i = 0; i < 24; i++) {
                const angle = rand(0, Math.PI * 2);
                const speed = rand(2, 7);
                targetParticles.push({
                    x: tx,
                    y: ty,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    color: shardColors[Math.floor(Math.random() * shardColors.length)],
                    size: rand(4, 10),
                    alpha: 1.0,
                    fade: rand(0.02, 0.05),
                    rot: rand(0, Math.PI),
                    rotSpeed: rand(-0.1, 0.1)
                });
            }
        }

        // --- Graphical Rendering Pipeline Functions (Realistic Shadows & Blending) ---
        function render() {
            ctx.save();
            
            // Apply Dynamic Screen Shake Juice
            if (screenShakeTime > 0) {
                const dx = rand(-7, 7);
                const dy = rand(-7, 7);
                ctx.translate(dx, dy);
            }

            drawEnvironmentBackground();
            drawTarget();
            drawBowStation();
            
            // Draw active flying arrows
            arrows.forEach(arrow => {
                drawArrow(arrow);
            });

            // Draw elastic bow string pull and trajectory projection
            if (drag.isDragging && activeArrow) {
                drawPullingString();
                drawTrajectory();
            }

            ctx.restore();
        }

        function drawEnvironmentBackground() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            let skyGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
            let groundGrad = ctx.createLinearGradient(0, 430, 0, canvas.height);

            switch (currentPlanetKey) {
                case 'earth':
                    // Earth: Soft blue gradient with dimensional cloudy forms
                    skyGrad.addColorStop(0, '#3b82f6');
                    skyGrad.addColorStop(1, '#93c5fd');
                    ctx.fillStyle = skyGrad;
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    // Draw volumetric atmospheric clouds
                    ctx.fillStyle = "rgba(255,255,255,0.45)";
                    drawCloud(200, 80, 40);
                    drawCloud(550, 110, 50);
                    
                    // Grassy shading terrain layer
                    groundGrad.addColorStop(0, '#22c55e');
                    groundGrad.addColorStop(1, '#15803d');
                    ctx.fillStyle = groundGrad;
                    ctx.fillRect(0, 430, canvas.width, 70);
                    break;

                case 'moon':
                    // Moon: Cosmic pitch deep space with procedural stellar maps
                    skyGrad.addColorStop(0, '#030712');
                    skyGrad.addColorStop(1, '#111827');
                    ctx.fillStyle = skyGrad;
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    // Draw random background star field clusters
                    ctx.fillStyle = "#ffffff";
                    for(let i=0; i<30; i++) {
                        let x = (i * 73) % canvas.width;
                        let y = (i * 29) % 350;
                        ctx.globalAlpha = 0.3 + (i % 5) * 0.15;
                        ctx.fillRect(x, y, 2, 2);
                    }
                    ctx.globalAlpha = 1.0;

                    // Cratering surface moon base map
                    groundGrad.addColorStop(0, '#6b7280');
                    groundGrad.addColorStop(1, '#374151');
                    ctx.fillStyle = groundGrad;
                    ctx.fillRect(0, 430, canvas.width, 70);
                    
                    // Detail textured moon crater maps with highlights & shading
                    ctx.fillStyle = '#4b5563';
                    ctx.strokeStyle = '#9ca3af';
                    ctx.lineWidth = 1;
                    drawCrater(120, 450, 25);
                    drawCrater(400, 445, 18);
                    drawCrater(680, 460, 30);
                    break;

                case 'mars':
                    // Mars: Dust iron-oxide oxidized skies
                    skyGrad.addColorStop(0, '#7c2d12');
                    skyGrad.addColorStop(1, '#ea580c');
                    ctx.fillStyle = skyGrad;
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    // Atmospheric suspended rust micro-debris dust particles
                    ctx.fillStyle = "rgba(234, 88, 12, 0.2)";
                    for(let i=0; i<15; i++) {
                        ctx.beginPath();
                        ctx.arc((i*97)%canvas.width, (i*41)%380, rand(3,8), 0, Math.PI*2);
                        ctx.fill();
                    }

                    // Desert base soils
                    groundGrad.addColorStop(0, '#c2410c');
                    groundGrad.addColorStop(1, '#431407');
                    ctx.fillStyle = groundGrad;
                    ctx.fillRect(0, 430, canvas.width, 70);
                    break;

                case 'venus':
                    // Venus: Intense thick sulfur fog with cracked hellscape volcanic rocks
                    skyGrad.addColorStop(0, '#422006');
                    skyGrad.addColorStop(1, '#ca8a04');
                    ctx.fillStyle = skyGrad;
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    // Dense chemical atmospheric mist overlay loops
                    let venusFog = ctx.createLinearGradient(0, 0, canvas.width, 0);
                    venusFog.addColorStop(0, 'rgba(161, 98, 7, 0.1)');
                    venusFog.addColorStop(0.5, 'rgba(234, 179, 8, 0.2)');
                    venusFog.addColorStop(1, 'rgba(161, 98, 7, 0.1)');
                    ctx.fillStyle = venusFog;
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    // Dark igneous basalts
                    groundGrad.addColorStop(0, '#1c1917');
                    groundGrad.addColorStop(1, '#0c0a09');
                    ctx.fillStyle = groundGrad;
                    ctx.fillRect(0, 430, canvas.width, 70);

                    // Molten lava fissures glowing in ground cracks
                    ctx.strokeStyle = '#f97316';
                    ctx.lineWidth = 3;
                    ctx.shadowColor = '#ef4444';
                    ctx.shadowBlur = 10;
                    ctx.beginPath();
                    for(let x=0; x<=canvas.width; x+=50) {
                        ctx.lineTo(x, 430 + (x%3==0 ? 15 : 5));
                    }
                    ctx.stroke();
                    ctx.shadowBlur = 0; // Reset blur state
                    break;

                case 'europa':
                    // Europa: Deep Jovian ice shelf with gas giant Jupiter scaling the backdrop
                    skyGrad.addColorStop(0, '#042f2e');
                    skyGrad.addColorStop(1, '#083344');
                    ctx.fillStyle = skyGrad;
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    // Rendering Jupiter sphere dynamically with band gradients & Great Red Spot
                    ctx.save();
                    let jupGrad = ctx.createLinearGradient(530, 40, 670, 180);
                    jupGrad.addColorStop(0, '#fed7aa');
                    jupGrad.addColorStop(0.3, '#fdba74');
                    jupGrad.addColorStop(0.6, '#ea580c');
                    jupGrad.addColorStop(1, '#7c2d12');
                    ctx.shadowColor = 'rgba(6, 182, 212, 0.4)';
                    ctx.shadowBlur = 30;
                    ctx.fillStyle = jupGrad;
                    ctx.beginPath();
                    ctx.arc(600, 110, 65, 0, Math.PI*2);
                    ctx.fill();
                    
                    // Jovian Storm lines details
                    ctx.fillStyle = "rgba(124, 45, 18, 0.3)";
                    ctx.fillRect(537, 90, 126, 8);
                    ctx.fillRect(535, 120, 130, 10);
                    // Great Red Spot
                    ctx.fillStyle = "#9a3412";
                    ctx.beginPath();
                    ctx.ellipse(620, 125, 12, 7, 0, 0, Math.PI*2);
                    ctx.fill();
                    ctx.restore();

                    // Glacial permafrost floor mapping
                    groundGrad.addColorStop(0, '#e0f2fe');
                    groundGrad.addColorStop(1, '#0284c7');
                    ctx.fillStyle = groundGrad;
                    ctx.fillRect(0, 430, canvas.width, 70);

                    // Subsurface crystalline cracks
                    ctx.strokeStyle = 'rgba(14, 116, 144, 0.5)';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(50, 430); ctx.lineTo(120, 470); ctx.lineTo(200, 440);
                    ctx.moveTo(400, 430); ctx.lineTo(430, 490);
                    ctx.moveTo(700, 430); ctx.lineTo(780, 465); ctx.lineTo(820, 445);
                    ctx.stroke();
                    break;
            }
        }

        function drawCloud(cx, cy, r) {
            ctx.beginPath();
            ctx.arc(cx, cy, r, 0, Math.PI*2);
            ctx.arc(cx - r*0.6, cy, r*0.7, 0, Math.PI*2);
            ctx.arc(cx + r*0.6, cy, r*0.7, 0, Math.PI*2);
            ctx.fill();
        }

        function drawCrater(cx, cy, r) {
            ctx.beginPath();
            ctx.arc(cx, cy, r, 0, Math.PI*2);
            ctx.fill();
            ctx.stroke();
        }

        function drawBowStation() {
            ctx.save();
            // Setup base stand geometry and shadows
            ctx.strokeStyle = '#4b5563';
            ctx.lineWidth = 5;
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(bow.x - 20, 430);
            ctx.lineTo(bow.x, bow.y);
            ctx.stroke();

            // Structural metallic nodes
            ctx.fillStyle = '#1f2937';
            ctx.beginPath();
            ctx.arc(bow.x, bow.y, 8, 0, Math.PI*2);
            ctx.fill();

            // Draw curved composite recurve bow limbs structure
            let bowAngle = 0;
            if (drag.isDragging) {
                bowAngle = Math.atan2(drag.startY - drag.currentY, drag.startX - drag.currentX) + Math.PI;
            }

            ctx.translate(bow.x, bow.y);
            ctx.rotate(bowAngle);

            ctx.strokeStyle = '#1e3a8a';
            ctx.lineWidth = 4;
            ctx.beginPath();
            // Arc representing bow body framework
            ctx.arc(-10, 0, bow.radius, -Math.PI/2.3, Math.PI/2.3, false);
            ctx.stroke();

            // Draw default relaxed bowstring rest alignment
            if (!drag.isDragging) {
                ctx.strokeStyle = 'rgba(156, 163, 175, 0.8)';
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(-10, -bow.radius * 0.9);
                ctx.lineTo(15, 0);
                ctx.lineTo(-10, bow.radius * 0.9);
                ctx.stroke();
            }

            ctx.restore();
            
            // Draw default resting arrow preview state on the launch shelf
            if (!drag.isDragging && activeArrow && isPlaying) {
                drawArrow(activeArrow);
            }
        }

        function drawPullingString() {
            ctx.save();
            // Track physical anchor nodes of dynamic string bending
            let bowAngle = Math.atan2(drag.startY - drag.currentY, drag.startX - drag.currentX) + Math.PI;
            
            ctx.translate(bow.x, bow.y);
            ctx.rotate(bowAngle);

            // Calculate precise terminal configurations of bow tips
            const topTipX = -10 + bow.radius * Math.cos(-Math.PI/2.3);
            const topTipY = bow.radius * Math.sin(-Math.PI/2.3);
            const botTipX = -10 + bow.radius * Math.cos(Math.PI/2.3);
            const botTipY = bow.radius * Math.sin(Math.PI/2.3);

            // Re-project global mouse coordinates inside the local rotated frame
            const localDragX = (drag.currentX - bow.x) * Math.cos(bowAngle) + (drag.currentY - bow.y) * Math.sin(bowAngle);
            const localDragY = -(drag.currentX - bow.x) * Math.sin(bowAngle) + (drag.currentY - bow.y) * Math.cos(bowAngle);

            ctx.strokeStyle = '#e5e7eb';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(topTipX, topTipY);
            ctx.lineTo(localDragX, localDragY);
            ctx.lineTo(botTipX, botTipY);
            ctx.stroke();

            ctx.restore();

            // Draw currently tensioned ready arrow inside drag state
            if(activeArrow) {
                activeArrow.x = drag.currentX;
                activeArrow.y = drag.currentY;
                activeArrow.angle = Math.atan2(drag.startY - drag.currentY, drag.startX - drag.currentX);
                drawArrow(activeArrow);
            }
        }

        function drawArrow(arrow) {
            ctx.save();
            ctx.translate(arrow.x, arrow.y);
            ctx.rotate(arrow.angle);

            // Shaft design
            ctx.strokeStyle = arrow.isApple ? '#b45309' : '#9ca3af'; // Wood shaft vs alloy silver
            ctx.lineWidth = 3;
            ctx.shadowColor = 'rgba(0,0,0,0.15)';
            ctx.shadowBlur = 3;
            ctx.beginPath();
            ctx.moveTo(-arrow.length / 2, 0);
            ctx.lineTo(arrow.length / 2, 0);
            ctx.stroke();

            // Metallic razor arrowhead tip
            ctx.fillStyle = '#4b5563';
            ctx.beginPath();
            ctx.moveTo(arrow.length / 2, 0);
            ctx.lineTo(arrow.length / 2 - 10, -5);
            ctx.lineTo(arrow.length / 2 - 10, 5);
            ctx.closePath();
            ctx.fill();

            // High-visibility rear fletching stabilizers
            ctx.fillStyle = arrow.isApple ? '#10b981' : '#ef4444';
            ctx.beginPath();
            ctx.moveTo(-arrow.length / 2, 0);
            ctx.lineTo(-arrow.length / 2 - 8, -6);
            ctx.lineTo(-arrow.length / 2 + 4, -6);
            ctx.lineTo(-arrow.length / 2 + 10, 0);
            ctx.lineTo(-arrow.length / 2 + 4, 6);
            ctx.lineTo(-arrow.length / 2 - 8, 6);
            ctx.closePath();
            ctx.fill();

            // SPECIAL MECHANIC: Apple Arrow Pierced Render
            if (arrow.isApple) {
                ctx.save();
                ctx.translate(arrow.length / 2 - 2, 0);
                
                // Draw realistic glossy structural red apple shell
                let appleGrad = ctx.createRadialGradient(-3, -3, 2, 0, 0, 10);
                appleGrad.addColorStop(0, '#f87171');
                appleGrad.addColorStop(0.8, '#dc2626');
                appleGrad.addColorStop(1, '#991b1b');
                ctx.fillStyle = appleGrad;
                ctx.beginPath();
                ctx.arc(0, 0, 9, 0, Math.PI*2);
                ctx.fill();

                // Detailed green structural foliage stem highlights
                ctx.strokeStyle = '#78350f';
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(0, -9);
                ctx.quadraticCurveTo(-3, -14, -5, -13);
                ctx.stroke();

                ctx.fillStyle = '#22c55e';
                ctx.beginPath();
                ctx.ellipse(-4, -13, 3, 1.5, Math.PI/4, 0, Math.PI*2);
                ctx.fill();

                ctx.restore();
            }

            ctx.restore();
        }

        function drawTrajectory() {
            if (!activeArrow) return;

            ctx.save();
            const env = environments[currentPlanetKey];
            const gPhysics = env.gravity * 2.5;
            const wPhysics = currentWind * 1.5;

            // Extract primary simulated vector forces matching the bow string pull angles
            const dx = drag.startX - drag.currentX;
            const dy = drag.startY - drag.currentY;
            const baseSpeedScale = 0.28;

            let simX = bow.x;
            let simY = bow.y;
            let simVx = dx * baseSpeedScale;
            let simVy = dy * baseSpeedScale;
            
            const timeStep = 0.16; // Incremental slice metrics for parabolic trace loops

            ctx.lineWidth = 3;
            ctx.setLineDash([4, 6]);

            // Adjust predictive trajectory color maps for Apple Arrow debuff
            if (activeArrow.isApple) {
                ctx.strokeStyle = 'rgba(239, 68, 68, 0.7)';
                // Inject real-time wobbly phase shifts to simulate the trajectory shake debuff
                simX += trajectoryShakeOffset.x;
                simY += trajectoryShakeOffset.y;
            } else {
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.65)';
            }

            ctx.beginPath();
            ctx.moveTo(simX, simY);

            // Extrapolate cinematic projection limits across 35 physical steps
            for (let step = 0; step < 35; step++) {
                simVx += wPhysics * timeStep;
                simVy += gPhysics * timeStep;
                simX += simVx * (timeStep * 60);
                simY += simVy * (timeStep * 60);

                ctx.lineTo(simX, simY);
                
                // Break trajectory lines if path clips terrain baseline boundaries
                if (simY > 430 || simX > canvas.width) break;
            }
            ctx.stroke();
            ctx.restore();
        }

        function drawTarget() {
            if (target.isDead) {
                // Execute rendering passes over shattered dynamic particle layers
                targetParticles.forEach(p => {
                    ctx.save();
                    ctx.globalAlpha = p.alpha;
                    ctx.fillStyle = p.color;
                    ctx.translate(p.x, p.y);
                    ctx.rotate(p.rot);
                    ctx.fillRect(-p.size/2, -p.size/2, p.size, p.size);
                    ctx.restore();
                });
                ctx.globalAlpha = 1.0;
                return;
            }

            ctx.save();
            ctx.translate(target.x, target.y);

            // Apply clear 3D drop-shadow highlights for target depth realism
            ctx.shadowColor = 'rgba(0,0,0,0.2)';
            ctx.shadowBlur = 12;
            ctx.shadowOffsetX = 5;
            ctx.shadowOffsetY = 5;

            // Zone D: Outer White Ring
            let gradD = ctx.createRadialGradient(-3, -3, 10, 0, 0, target.radiusD);
            gradD.addColorStop(0, '#ffffff');
            gradD.addColorStop(0.8, '#f3f4f6');
            gradD.addColorStop(1, '#d1d5db');
            ctx.fillStyle = gradD;
            ctx.beginPath();
            ctx.arc(0, 0, target.radiusD, 0, Math.PI*2);
            ctx.fill();
            ctx.strokeStyle = '#9ca3af';
            ctx.lineWidth = 1;
            ctx.stroke();

            // Zone C: Medium Black Ring
            let gradC = ctx.createRadialGradient(-2, -2, 5, 0, 0, target.radiusC);
            gradC.addColorStop(0, '#4b5563');
            gradC.addColorStop(0.7, '#1f2937');
            gradC.addColorStop(1, '#111827');
            ctx.fillStyle = gradC;
            ctx.beginPath();
            ctx.arc(0, 0, target.radiusC, 0, Math.PI*2);
            ctx.fill();

            // Zone B: Medium-Small Crimson Ring
            let gradB = ctx.createRadialGradient(-2, -2, 3, 0, 0, target.radiusB);
            gradB.addColorStop(0, '#f87171');
            gradB.addColorStop(0.7, '#dc2626');
            gradB.addColorStop(1, '#991b1b');
            ctx.fillStyle = gradB;
            ctx.beginPath();
            ctx.arc(0, 0, target.radiusB, 0, Math.PI*2);
            ctx.fill();

            // Zone A: Gold Bullseye Core
            ctx.shadowBlur = 0; // Remove sub-shadow layers to intensify crisp metallic look
            ctx.shadowOffsetX = 0;
            ctx.shadowOffsetY = 0;
            let gradA = ctx.createRadialGradient(-2, -2, 1, 0, 0, target.radiusA);
            gradA.addColorStop(0, '#fef08a');
            gradA.addColorStop(0.6, '#eab308');
            gradA.addColorStop(1, '#a16207');
            ctx.fillStyle = gradA;
            ctx.beginPath();
            ctx.arc(0, 0, target.radiusA, 0, Math.PI*2);
            ctx.fill();

            // Concentric crisp ring split lines mapping
            ctx.strokeStyle = 'rgba(255,255,255,0.25)';
            ctx.lineWidth = 1.5;
            ctx.beginPath(); ctx.arc(0, 0, target.radiusB, 0, Math.PI*2); ctx.stroke();
            ctx.beginPath(); ctx.arc(0, 0, target.radiusC, 0, Math.PI*2); ctx.stroke();
            ctx.strokeStyle = 'rgba(0,0,0,0.15)';
            ctx.beginPath(); ctx.arc(0, 0, target.radiusA, 0, Math.PI*2); ctx.stroke();

            ctx.restore();
        }

        // Trigger bootstrap configuration sequences
        initEnvironment();
        render();

    </script>
</body>
</html>
"""

# Render the self-contained HTML/JS application viewport via the Streamlit Component Bridge
st.components.v1.html(game_code, height=660, scrolling=False)

# Educational physics formulas section explaining the simulation engine variables
st.markdown("---")
st.markdown(
    """
    ### 🌌 그래비티 애로우 물리학 노트 (Physics Documentation)
    본 시뮬레이션 게임은 각 천체의 고유 환경 데이터를 기반으로 수평 및 수직 방향의 역학 법칙을 실시간으로 계산합니다.
    
    1. **포물선 이동 방정식 (Projective Kinematics)**:
       화살이 발사된 후 매 프레임($\\Delta t$)마다 아래의 상태 변화 방정식에 따라 화살의 속도 벡터와 위치 좌표가 업데이트됩니다.
       $$v_x(t + \\Delta t) = v_x(t) + a_{wind} \\cdot \\Delta t$$
       $$v_y(t + \\Delta t) = v_y(t) + g_{planet} \\cdot \\Delta t$$
       $$x(t + \\Delta t) = x(t) + v_x \\cdot \\Delta t,\\quad y(t + \\Delta t) = y(t) + v_y \\cdot \\Delta t$$
    
    2. **천체별 환경 특성**:
       * **지구 (Earth)**: 표준 중력 가속도($9.8\\text{ m/s}^2$)와 적당한 풍속 저항이 작용하여 가장 직관적인 포물선 궤적을 그립니다.
       * **달 (Moon)**: 대기가 전혀 없는 진공 환경($0\\text{ m/s}$)이며, 지구 중력의 약 $1/6$ 수준($1.6\\text{ m/s}^2$)으로 작용하므로 화살이 매우 완만하고 길게 비행합니다.
       * **화성 (Mars)**: 희박한 대기 속에서 약한 중력($3.7\\text{ m/s}^2$)이 작용하여 낙하 속도가 느립니다.
       * **금성 (Venus)**: 매우 농밀하고 무거운 황산 대기를 시뮬레이션하여 임의의 강한 돌풍과 기류 저항($\\pm 4.0\\text{ m/s}$)이 화살의 수평 궤적을 크게 뒤흔듭니다.
       * **유로파 (Europa)**: 목성의 강력한 조석력 영향을 받는 얼음 위성으로, 매우 낮은 중력($1.3\\text{ m/s}^2$) 환경에서 거대한 목성을 배경으로 정밀한 저중력 사격을 연습할 수 있습니다.
    
    3. **애플 애로우 (Apple Arrow) 메커니즘**:
       * **순간 점수 버프**: 과녁 적중 시 획득하는 점수가 즉시 **2배(2x)**로 증가합니다.
       * **궤적 불확정성 디버프**: 사과 자체의 공기 유체 역학적 불안정성으로 인해 예측 점선 궤적이 **1초마다 무작위로 흔들려(Wobble)** 정밀 조준을 방해하도록 설계되었습니다.
    """
)
