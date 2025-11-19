(function () {
    const canvas = document.getElementById('contra-canvas');
    if (!canvas) {
        return;
    }

    const ctx = canvas.getContext('2d');
    const FLOOR = canvas.height - 70;

    const dom = {
        levelName: document.getElementById('contra-level-name'),
        levelStatus: document.getElementById('contra-level-status'),
        health: document.getElementById('contra-health'),
        enemies: document.getElementById('contra-enemies'),
        combo: document.getElementById('contra-combo'),
        score: document.getElementById('contra-score'),
        intelTitle: document.getElementById('contra-intel-title'),
        intelDesc: document.getElementById('contra-intel-desc'),
        intelList: document.getElementById('contra-intel-list'),
        progress: document.getElementById('level-progress'),
        feed: document.getElementById('intel-feed'),
        btnStart: document.getElementById('contra-start'),
        btnReset: document.getElementById('contra-reset'),
        btnMute: document.getElementById('contra-mute'),
        mobileButtons: document.querySelectorAll('.mobile-buttons button')
    };

    class AudioManager {
        constructor() {
            this.enabled = true;
            this.context = null;
            this.themeInterval = null;
        }

        init() {
            if (this.context || !window.AudioContext) return;
            this.context = new (window.AudioContext || window.webkitAudioContext)();
        }

        playSynth(options = {}) {
            if (!this.enabled) return;
            this.init();
            if (!this.context) return;

            const {
                frequency = 220,
                duration = 0.2,
                type = 'square',
                gain = 0.18,
                detune = 0
            } = options;

            const osc = this.context.createOscillator();
            const gainNode = this.context.createGain();
            osc.type = type;
            osc.frequency.value = frequency;
            osc.detune.value = detune;

            gainNode.gain.value = gain;
            gainNode.gain.exponentialRampToValueAtTime(0.0001, this.context.currentTime + duration);

            osc.connect(gainNode).connect(this.context.destination);
            osc.start();
            osc.stop(this.context.currentTime + duration);
        }

        playEffect(effect) {
            if (!this.enabled) return;
            const map = {
                shoot: () => this.playSynth({ frequency: 520, duration: 0.08, type: 'sawtooth', gain: 0.15 }),
                hit: () => this.playSynth({ frequency: 180, duration: 0.2, type: 'triangle', gain: 0.2 }),
                enemyDown: () => this.playSynth({ frequency: 320, duration: 0.25, type: 'square', gain: 0.22 }),
                jump: () => this.playSynth({ frequency: 260, duration: 0.18, type: 'triangle', gain: 0.12 }),
                combo: () => this.playSynth({ frequency: 640, duration: 0.15, type: 'square', gain: 0.18 }),
                boss: () => this.playSynth({ frequency: 140, duration: 0.45, type: 'sawtooth', gain: 0.25 }),
                victory: () => this.playSynth({ frequency: 440, duration: 0.5, type: 'triangle', gain: 0.25 })
            };
            map[effect]?.();
        }

        playTheme() {
            if (!this.enabled || this.themeInterval) return;
            this.init();
            if (!this.context) return;
            const notes = [196, 233, 294, 349, 392];
            let index = 0;
            this.themeInterval = setInterval(() => {
                this.playSynth({
                    frequency: notes[index % notes.length],
                    duration: 0.14,
                    type: 'triangle',
                    gain: 0.12
                });
                index += 1;
            }, 220);
        }

        stopTheme() {
            if (this.themeInterval) {
                clearInterval(this.themeInterval);
                this.themeInterval = null;
            }
        }

        toggle() {
            this.enabled = !this.enabled;
            if (!this.enabled) {
                this.stopTheme();
            } else if (state.active) {
                this.playTheme();
            }
            return this.enabled;
        }
    }

    const audio = new AudioManager();

    const LEVELS = [
        {
            name: '雨林突袭',
            intel: '切入赤焰雨林，摧毁信号塔并击退迷彩小队。藤蔓地形会降低敌军跳跃高度。',
            bullets: [
                '波次：迷彩步兵 x6、爆裂机枪手 x3、浮空侦察机 x2',
                '目标：在 90 秒内突破防线并击落「藤蔓炮塔」',
                '提示：爆裂机枪手的射速慢但弹道穿透，可优先秒杀'
            ],
            waves: [
                { type: 'grunt', count: 6 },
                { type: 'jumper', count: 3 },
                { type: 'turret', count: 1 },
                { type: 'drone', count: 2 }
            ],
            boss: { type: 'vines', hp: 36, fireRate: 1.4 }
        },
        {
            name: '冰原要塞',
            intel: '极寒风暴覆盖装甲车队，敌军导弹无人机会在半空引爆。保持移动避免被冰面牵制。',
            bullets: [
                '波次：雪地步兵 x8、滑铲突击 x4、导弹无人机 x3',
                '目标：击毁「寒噬巨炮」并截获能源舱',
                '提示：滑铲突击会突然贴脸，可用空中火力预判点杀'
            ],
            waves: [
                { type: 'grunt', count: 4 },
                { type: 'jumper', count: 4 },
                { type: 'drone', count: 3 },
                { type: 'turret', count: 2 }
            ],
            boss: { type: 'cannon', hp: 46, fireRate: 1.1 }
        },
        {
            name: '赤色终端',
            intel: '潜入空港塔顶，终结 AI 指挥核心。敌方将动用全频电磁炮和忍者部队进行阻拦。',
            bullets: [
                '波次：赤刃忍者 x6、激光浮雷 x4、盾兵 x4',
                '目标：击破「天穹终端」完成 EMP 注入',
                '提示：连击条满格即可释放必杀，清屏并削弱头目护盾'
            ],
            waves: [
                { type: 'jumper', count: 6 },
                { type: 'grunt', count: 4 },
                { type: 'turret', count: 2 },
                { type: 'drone', count: 4 }
            ],
            boss: { type: 'terminal', hp: 60, fireRate: 0.9 }
        }
    ];

    const keys = new Set();
    const inputs = { left: false, right: false, jump: false, fire: false };

    function handleKey(code, pressed, originalEvent) {
        const prevent = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'];
        if (prevent.includes(code)) {
            originalEvent?.preventDefault?.();
        }

        if (['ArrowLeft', 'KeyA'].includes(code)) inputs.left = pressed;
        if (['ArrowRight', 'KeyD'].includes(code)) inputs.right = pressed;
        if (['ArrowUp', 'KeyW', 'Space'].includes(code)) inputs.jump = pressed;
        if (['KeyJ', 'KeyK', 'ControlLeft', 'ControlRight'].includes(code)) inputs.fire = pressed;
    }

    window.addEventListener('keydown', (e) => {
        if (e.repeat) return;
        keys.add(e.code);
        handleKey(e.code, true, e);

        if (e.code === 'Enter' && !state.active) {
            startMission();
        }
        if (e.code === 'Escape') {
            state.paused = !state.paused;
            addIntel(state.paused ? '暂停作战。' : '恢复作战。');
        }
        if (e.code === 'KeyP') {
            state.slowMotion = !state.slowMotion;
            addIntel(state.slowMotion ? '教学慢动作已开启。' : '恢复实时速度。');
        }
        if (e.code === 'KeyL' && state.superMeter >= 1) {
            unleashNova();
        }
    });

    window.addEventListener('keyup', (e) => {
        keys.delete(e.code);
        handleKey(e.code, false, e);
    });

    function bindMobileButtons() {
        dom.mobileButtons.forEach((btn) => {
            const action = btn.dataset.action;
            const press = (pressed) => {
                if (action === 'left') inputs.left = pressed;
                if (action === 'right') inputs.right = pressed;
                if (action === 'jump') inputs.jump = pressed;
                if (action === 'fire') inputs.fire = pressed;
                if (!state.active && pressed) {
                    startMission();
                }
            };
            btn.addEventListener('touchstart', (e) => {
                e.preventDefault();
                press(true);
            }, { passive: false });
            btn.addEventListener('touchend', (e) => {
                e.preventDefault();
                press(false);
            }, { passive: false });
        });
    }

    bindMobileButtons();

    class Player {
        constructor() {
            this.reset();
        }

        reset() {
            this.x = 80;
            this.y = FLOOR - 56;
            this.vx = 0;
            this.vy = 0;
            this.width = 40;
            this.height = 56;
            this.speed = 3.2;
            this.jumpForce = -11.2;
            this.onGround = true;
            this.health = 5;
            this.cooldown = 0;
            this.superReady = false;
        }

        move(delta) {
            const acceleration = 0.55 * delta;
            if (inputs.left) this.vx -= acceleration;
            if (inputs.right) this.vx += acceleration;
            if (!inputs.left && !inputs.right) this.vx *= 0.85;

            this.vx = Math.max(-5.2, Math.min(5.2, this.vx));
            this.x += this.vx * delta;
            this.x = Math.max(24, Math.min(canvas.width - 60, this.x));

            if (inputs.jump && this.onGround) {
                this.vy = this.jumpForce;
                this.onGround = false;
                audio.playEffect('jump');
            }

            this.vy += 0.55 * delta;
            this.y += this.vy * delta * 0.9;
            if (this.y + this.height >= FLOOR) {
                this.y = FLOOR - this.height;
                this.vy = 0;
                this.onGround = true;
            }

            if (this.cooldown > 0) {
                this.cooldown -= 0.016 * delta;
            }

            if (inputs.fire && this.cooldown <= 0) {
                this.shoot();
            }
        }

        shoot(power = 1) {
            state.projectiles.push(new Projectile(
                this.x + this.width - 6,
                this.y + this.height / 2,
                7.6 * power,
                0,
                'player',
                1 * power
            ));
            this.cooldown = 0.2;
            audio.playEffect('shoot');
        }

        draw() {
            ctx.save();
            ctx.fillStyle = '#38bdf8';
            ctx.fillRect(this.x, this.y, this.width, this.height);
            ctx.fillStyle = '#0ea5e9';
            ctx.fillRect(this.x + 6, this.y + 8, this.width - 12, this.height - 24);
            ctx.fillStyle = '#f97316';
            ctx.fillRect(this.x + this.width - 6, this.y + 24, 12, 6);
            ctx.restore();
        }
    }

    class Projectile {
        constructor(x, y, vx, vy, owner, damage = 1) {
            this.x = x;
            this.y = y;
            this.vx = vx;
            this.vy = vy;
            this.owner = owner;
            this.damage = damage;
            this.width = owner === 'player' ? 12 : 6;
            this.height = 4;
            this.active = true;
        }

        update(delta) {
            this.x += this.vx * delta;
            this.y += this.vy * delta;

            if (this.x > canvas.width + 50 || this.x < -50 || this.y < -50 || this.y > canvas.height + 50) {
                this.active = false;
            }
        }

        draw() {
            ctx.fillStyle = this.owner === 'player' ? '#fbbf24' : '#f43f5e';
            ctx.fillRect(this.x, this.y, this.width, this.height);
        }
    }

    class Enemy {
        constructor(type) {
            const baseY = FLOOR - 48;
            this.type = type;
            this.active = true;
            this.direction = Math.random() > 0.5 ? -1 : 1;
            this.fireCooldown = 1.2;

            const presets = {
                grunt: { width: 34, height: 48, speed: 1.5, hp: 2, reward: 120 },
                jumper: { width: 32, height: 46, speed: 2.3, hp: 3, reward: 160 },
                turret: { width: 40, height: 52, speed: 0.2, hp: 5, reward: 220 },
                drone: { width: 30, height: 30, speed: 1.4, hp: 2, reward: 180 }
            };

            Object.assign(this, presets[type] || presets.grunt);

            this.x = canvas.width + Math.random() * 160;
            this.y = type === 'drone' ? 140 + Math.random() * 120 : baseY;
            this.vy = 0;
            this.jumpTimer = Math.random() * 1.5;
        }

        update(delta) {
            if (!this.active) return;
            if (this.type === 'drone') {
                this.y += Math.sin(Date.now() / 400) * 0.6 * delta;
            } else if (this.type === 'jumper') {
                this.jumpTimer -= 0.016 * delta;
                if (this.jumpTimer <= 0 && this.y + this.height >= FLOOR) {
                    this.vy = -8.5;
                    this.jumpTimer = 1.8 + Math.random();
                }
                this.vy += 0.45 * delta;
                this.y += this.vy * delta;
                if (this.y + this.height >= FLOOR) {
                    this.y = FLOOR - this.height;
                    this.vy = 0;
                }
            }

            if (this.type !== 'turret') {
                this.x += this.speed * delta * this.direction;
                if (this.x < 340) this.direction = 1;
                if (this.x > canvas.width - 60) this.direction = -1;
            }

            this.fireCooldown -= 0.016 * delta;
            if (this.fireCooldown <= 0) {
                this.fireCooldown = this.type === 'turret' ? 1.6 : (this.type === 'drone' ? 1 : 2.2);
                if (Math.random() < 0.65) {
                    this.shoot();
                }
            }
        }

        shoot() {
            const speed = this.type === 'drone' ? -3.3 : -4.5;
            state.projectiles.push(new Projectile(
                this.x,
                this.y + this.height / 2,
                speed,
                this.type === 'drone' ? (Math.random() - 0.5) * 1.5 : (Math.random() * 0.8 - 0.4),
                'enemy',
                1
            ));
        }

        draw() {
            ctx.fillStyle = {
                grunt: '#f87171',
                jumper: '#fb923c',
                turret: '#f43f5e',
                drone: '#c084fc'
            }[this.type] || '#f87171';
            ctx.fillRect(this.x, this.y, this.width, this.height);
            ctx.fillStyle = '#1e1b4b';
            ctx.fillRect(this.x + 4, this.y + 6, this.width - 8, this.height - 12);
        }
    }

    class Boss {
        constructor(config) {
            this.type = config.type;
            this.hp = config.hp;
            this.maxHp = config.hp;
            this.fireRate = config.fireRate;
            this.x = canvas.width - 220;
            this.y = 120;
            this.width = 180;
            this.height = 120;
            this.cooldown = 0.5;
            this.active = true;
        }

        update(delta) {
            if (!this.active) return;
            this.x += Math.sin(Date.now() / 500) * 0.4 * delta;
            this.y += Math.cos(Date.now() / 600) * 0.35 * delta;

            this.cooldown -= 0.016 * delta;
            if (this.cooldown <= 0) {
                this.cooldown = this.fireRate;
                this.fire();
            }
        }

        fire() {
            const pattern = Math.random();
            if (pattern < 0.4) {
                for (let i = 0; i < 3; i++) {
                    state.projectiles.push(new Projectile(
                        this.x,
                        this.y + 20 * (i + 1),
                        -4.5,
                        (i - 1) * 0.9,
                        'enemy',
                        1.5
                    ));
                }
            } else {
                state.projectiles.push(new Projectile(
                    this.x,
                    this.y + this.height / 2,
                    -6,
                    0,
                    'enemy',
                    2
                ));
            }
        }

        draw() {
            ctx.fillStyle = '#facc15';
            ctx.fillRect(this.x, this.y, this.width, this.height);
            ctx.fillStyle = '#f97316';
            ctx.fillRect(this.x + 12, this.y + 12, this.width - 24, this.height - 24);
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(this.x + 40, this.y + 30, this.width - 80, this.height - 60);

            const ratio = this.hp / this.maxHp;
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(this.x, this.y - 14, this.width, 6);
            ctx.fillStyle = '#ef4444';
            ctx.fillRect(this.x, this.y - 14, this.width * ratio, 6);
        }
    }

    const player = new Player();

    const state = {
        active: false,
        paused: false,
        slowMotion: false,
        currentLevel: 0,
        score: 0,
        combo: 0,
        comboTimer: 0,
        superMeter: 0,
        enemies: [],
        projectiles: [],
        particles: [],
        boss: null,
        waveIndex: 0,
        defeated: 0,
        totalTargets: 0,
        remaining: 0,
        levelTimer: 0
    };

    function addIntel(message) {
        if (!dom.feed) return;
        const entry = document.createElement('div');
        entry.className = 'feed-item';
        entry.innerHTML = `<strong>HQ</strong> · ${message}`;
        dom.feed.prepend(entry);
        while (dom.feed.children.length > 8) {
            dom.feed.removeChild(dom.feed.lastChild);
        }
    }

    function updateIntelPanel(level) {
        dom.levelName.textContent = level?.name ?? '-';
        dom.intelDesc.textContent = level?.intel ?? '——';
        dom.intelList.innerHTML = '';
        (level?.bullets || []).forEach((tip) => {
            const li = document.createElement('li');
            li.textContent = tip;
            dom.intelList.appendChild(li);
        });
    }

    function resetGame(fullReset = true) {
        state.active = false;
        state.paused = false;
        state.slowMotion = false;
        state.projectiles = [];
        state.enemies = [];
        state.particles = [];
        state.boss = null;
        state.waveIndex = 0;
        state.defeated = 0;
        state.remaining = 0;
        state.combo = 0;
        state.comboTimer = 0;
        state.superMeter = 0;

        if (fullReset) {
            state.currentLevel = 0;
            state.score = 0;
        }

        dom.levelStatus.textContent = '休整';
        dom.progress.style.width = '0%';
        dom.enemies.textContent = '0';
        dom.combo.textContent = 'x0';
        dom.health.textContent = player.health;

        player.reset();
        document.body.classList.add('contra-mode');
        updateIntelPanel(LEVELS[state.currentLevel]);
        addIntel('战局已经重置，等待新任务。');
    }

    function startMission() {
        audio.init();
        audio.playTheme();
        document.body.classList.add('contra-mode');
        dom.levelStatus.textContent = '作战中';
        state.active = true;
        state.paused = false;
        state.waveIndex = 0;
        state.defeated = 0;
        state.projectiles = [];
        state.enemies = [];
        state.boss = null;
        state.superMeter = 0;
        state.combo = 0;
        state.levelTimer = 0;

        const level = LEVELS[state.currentLevel];
        state.totalTargets = level.waves.reduce((sum, w) => sum + w.count, 0) + 1;
        state.remaining = state.totalTargets;

        updateIntelPanel(level);
        addIntel(`「${level.name}」行动开始。`);
        spawnNextWave();
    }

    function spawnNextWave() {
        const level = LEVELS[state.currentLevel];
        const wave = level.waves[state.waveIndex];
        if (wave) {
            for (let i = 0; i < wave.count; i += 1) {
                state.enemies.push(new Enemy(wave.type));
            }
            state.waveIndex += 1;
            addIntel(`新波次抵达：${wave.type} x${wave.count}`);
        } else if (!state.boss) {
            state.boss = new Boss(level.boss);
            audio.playEffect('boss');
            addIntel('警告：头目出现！');
        }
    }

    function unleashNova() {
        state.superMeter = 0;
        state.projectiles.push(new Projectile(
            player.x + player.width,
            player.y,
            12,
            0,
            'player',
            4
        ));
        state.enemies.forEach((enemy) => {
            enemy.hp -= 3;
            if (enemy.hp <= 0 && enemy.active) {
                handleEnemyDown(enemy);
            }
        });
        if (state.boss) {
            state.boss.hp -= 5;
            if (state.boss.hp <= 0) {
                state.boss.active = false;
            }
        }
        audio.playEffect('combo');
        addIntel('必杀 · 雷鸣冲击释放！');
    }

    function handleEnemyDown(enemy) {
        enemy.active = false;
        state.defeated += 1;
        state.remaining = Math.max(0, state.totalTargets - state.defeated);
        state.score += enemy.reward;
        state.combo = Math.min(12, state.combo + 1);
        state.comboTimer = 3;
        state.superMeter = Math.min(1, state.superMeter + 0.2);
        audio.playEffect('enemyDown');
        updateProgress();
        addIntel(`击倒 ${enemy.type}，获得 ${enemy.reward} 分。`);
    }

    function updateProgress() {
        const ratio = state.defeated / state.totalTargets;
        dom.progress.style.width = `${(ratio * 100).toFixed(2)}%`;
        dom.enemies.textContent = state.remaining.toString();
        dom.score.textContent = state.score.toString();
        dom.combo.textContent = `x${state.combo}`;
    }

    function updateGame(delta) {
        if (state.paused) return;
        const speedFactor = state.slowMotion ? 0.4 : 1;
        delta *= speedFactor;

        player.move(delta);
        dom.health.textContent = player.health;

        state.enemies.forEach((enemy) => enemy.update(delta));
        state.projectiles.forEach((proj) => proj.update(delta));
        state.projectiles = state.projectiles.filter((p) => p.active);

        if (state.boss) {
            state.boss.update(delta);
        }

        handleCollisions();

        if (state.enemies.every((e) => !e.active) && (!state.boss || !state.boss.active)) {
            if (state.waveIndex < LEVELS[state.currentLevel].waves.length) {
                spawnNextWave();
            } else if (state.boss && state.boss.active) {
                // waiting
            } else {
                handleLevelClear();
            }
        }

        if (state.combo > 0) {
            state.comboTimer -= 0.016 * delta;
            if (state.comboTimer <= 0) {
                state.combo = Math.max(0, state.combo - 1);
                state.comboTimer = 1.2;
                dom.combo.textContent = `x${state.combo}`;
            }
        }
    }

    function handleCollisions() {
        state.projectiles.forEach((projectile) => {
            if (!projectile.active) return;

            if (projectile.owner === 'player') {
                state.enemies.forEach((enemy) => {
                    if (!enemy.active) return;
                    if (rectsOverlap(projectile, enemy)) {
                        projectile.active = false;
                        enemy.hp -= projectile.damage;
                        if (enemy.hp <= 0) {
                            handleEnemyDown(enemy);
                        } else {
                            audio.playEffect('hit');
                        }
                    }
                });

                if (state.boss && state.boss.active && rectsOverlap(projectile, state.boss)) {
                    projectile.active = false;
                    state.boss.hp -= projectile.damage;
                    audio.playEffect('hit');
                    if (state.boss.hp <= 0) {
                        state.boss.active = false;
                        state.defeated += 1;
                        state.remaining = Math.max(0, state.totalTargets - state.defeated);
                        updateProgress();
                        addIntel('头目被摧毁！');
                        audio.playEffect('victory');
                    }
                }
            } else {
                if (rectsOverlap(projectile, player)) {
                    projectile.active = false;
                    player.health -= 1;
                    dom.health.textContent = player.health;
                    audio.playEffect('hit');
                    addIntel('收到命中！注意机动。');
                    if (player.health <= 0) {
                        handlePlayerDown();
                    }
                }
            }
        });
    }

    function rectsOverlap(a, b) {
        return a.x < b.x + b.width &&
            a.x + a.width > b.x &&
            a.y < b.y + b.height &&
            a.y + a.height > b.y;
    }

    function handlePlayerDown() {
        state.active = false;
        audio.stopTheme();
        dom.levelStatus.textContent = '阵亡';
        addIntel('任务失败，按「开始任务」重试。');
    }

    function handleLevelClear() {
        audio.playEffect('victory');
        addIntel(`阶段「${LEVELS[state.currentLevel].name}」已清理。`);
        state.currentLevel += 1;
        if (state.currentLevel >= LEVELS.length) {
            dom.levelStatus.textContent = '全胜';
            audio.stopTheme();
            addIntel('恭喜通关所有关卡！可继续挑战以刷新分数。');
            state.currentLevel = LEVELS.length - 1;
            state.active = false;
            return;
        }
        state.active = false;
        dom.levelStatus.textContent = '完成';
        addIntel('准备前往下一战区。');
        updateIntelPanel(LEVELS[state.currentLevel]);
    }

    function drawBackground() {
        ctx.fillStyle = '#020617';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
        grad.addColorStop(0, '#0f172a');
        grad.addColorStop(0.6, '#1e293b');
        grad.addColorStop(1, '#0f172a');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = 'rgba(15,23,42,0.9)';
        ctx.fillRect(0, FLOOR, canvas.width, canvas.height - FLOOR);

        ctx.fillStyle = 'rgba(248,113,113,0.15)';
        for (let i = 0; i < canvas.width; i += 60) {
            ctx.fillRect((i + (Date.now() / 40) % 60), FLOOR - 6, 20, 6);
        }
    }

    function drawGame() {
        drawBackground();
        player.draw();
        state.enemies.forEach((enemy) => enemy.draw());
        state.projectiles.forEach((proj) => proj.draw());
        if (state.boss && state.boss.active) {
            state.boss.draw();
        }

        ctx.fillStyle = '#f1f5f9';
        ctx.font = '16px "Consolas", monospace';
        ctx.fillText(`LEVEL ${state.currentLevel + 1} · SCORE ${state.score}`, 20, 30);
        ctx.fillText(`HP ${player.health} · COMBO x${state.combo}`, 20, 50);
        ctx.fillText(`SUPER ${(state.superMeter * 100).toFixed(0)}%`, 20, 70);
    }

    let lastTime = 0;
    function loop(timestamp) {
        const delta = (timestamp - lastTime) / (1000 / 60) || 1;
        lastTime = timestamp;
        if (state.active) {
            updateGame(delta);
        }
        drawGame();
        requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);

    dom.btnStart?.addEventListener('click', () => startMission());
    dom.btnReset?.addEventListener('click', () => resetGame(false));
    dom.btnMute?.addEventListener('click', () => {
        const enabled = audio.toggle();
        dom.btnMute.textContent = `音效：${enabled ? '开启' : '静音'}`;
    });

    resetGame();
})();