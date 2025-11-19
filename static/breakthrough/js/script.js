(() => {
  const canvas = document.getElementById("nebula-canvas");
  const ctx = canvas.getContext("2d");

  const ui = {
    level: document.getElementById("level"),
    score: document.getElementById("score"),
    shield: document.getElementById("shield"),
    combo: document.getElementById("combo"),
    mode: document.getElementById("mode-label"),
    pulse: document.getElementById("pulse-status"),
    meteor: document.getElementById("meteor-status"),
    boost: document.getElementById("boost-status"),
    feed: document.getElementById("mission-feed")
  };

  const buttons = {
    pause: document.getElementById("pause-btn"),
    resume: document.getElementById("resume-btn"),
    restart: document.getElementById("restart-btn"),
    pulse: document.getElementById("pulse-btn"),
    difficulty: [...document.querySelectorAll("#difficulty-buttons .chip")]
  };

  const WIDTH = canvas.width;
  const HEIGHT = canvas.height;
  const MAX_FEED = 6;
  const LOCAL_KEY = "neon-runner-highscore";

  const colors = {
    player: "#7af5ff",
    orb: "#ffe761",
    drone: "#ff8df4",
    meteor: "#ff5757",
    shield: "#61f2ff",
    text: "rgba(234, 241, 255, 0.9)"
  };

  const DIFFICULTIES = {
    casual: {
      label: "Casual",
      shield: 5,
      droneFactor: 0.7,
      meteorInterval: [8, 14],
      powerupInterval: [5, 9],
      pulseCooldown: 7
    },
    voyager: {
      label: "Voyager",
      shield: 4,
      droneFactor: 1,
      meteorInterval: [6, 11],
      powerupInterval: [7, 11],
      pulseCooldown: 8
    },
    eclipse: {
      label: "Eclipse",
      shield: 3,
      droneFactor: 1.35,
      meteorInterval: [4, 8],
      powerupInterval: [9, 13],
      pulseCooldown: 9
    }
  };

  class Entity {
    constructor(x, y, radius) {
      this.x = x;
      this.y = y;
      this.radius = radius;
    }
  }

  class Player extends Entity {
    constructor() {
      super(WIDTH / 2, HEIGHT / 2, 16);
      this.baseSpeed = 260;
      this.speedMultiplier = 1;
      this.boostTimer = 0;
      this.pulseVisual = 0;
    }

    update(dt, input) {
      const dir = { x: 0, y: 0 };
      if (input.up) dir.y -= 1;
      if (input.down) dir.y += 1;
      if (input.left) dir.x -= 1;
      if (input.right) dir.x += 1;
      const length = Math.hypot(dir.x, dir.y) || 1;
      const speed = this.baseSpeed * this.speedMultiplier;
      this.x += (dir.x / length) * speed * dt;
      this.y += (dir.y / length) * speed * dt;
      this.x = Math.min(Math.max(this.radius, this.x), WIDTH - this.radius);
      this.y = Math.min(Math.max(this.radius, this.y), HEIGHT - this.radius);

      if (this.boostTimer > 0) {
        this.boostTimer -= dt;
        if (this.boostTimer <= 0) {
          this.speedMultiplier = 1;
        }
      }

      if (this.pulseVisual > 0) {
        this.pulseVisual -= dt;
      }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = colors.player;
      ctx.shadowBlur = 20;
      ctx.shadowColor = colors.player;
      ctx.fill();
      ctx.shadowBlur = 0;

      if (this.pulseVisual > 0) {
        ctx.beginPath();
        const radius = this.radius + (1 - this.pulseVisual / 0.4) * 180;
        ctx.arc(this.x, this.y, radius, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(122, 245, 255, ${this.pulseVisual / 0.4})`;
        ctx.lineWidth = 3;
        ctx.stroke();
      }
    }

    applyBoost(multiplier, duration) {
      this.speedMultiplier = multiplier;
      this.boostTimer = duration;
    }

    triggerPulseVisual() {
      this.pulseVisual = 0.4;
    }
  }

  class Orb extends Entity {
    constructor() {
      const padding = 40;
      super(
        padding + Math.random() * (WIDTH - padding * 2),
        padding + Math.random() * (HEIGHT - padding * 2),
        10
      );
      this.pulse = Math.random() * Math.PI * 2;
    }
    update(dt) {
      this.pulse += dt * 4;
    }
    draw() {
      const size = this.radius + Math.sin(this.pulse) * 2;
      ctx.beginPath();
      ctx.arc(this.x, this.y, size, 0, Math.PI * 2);
      ctx.fillStyle = colors.orb;
      ctx.shadowBlur = 12;
      ctx.shadowColor = colors.orb;
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }

  class Drone extends Entity {
    constructor(speedMultiplier) {
      const border = 30;
      super(
        Math.random() < 0.5 ? border : WIDTH - border,
        border + Math.random() * (HEIGHT - border * 2),
        18
      );
      const angle = Math.random() * Math.PI * 2;
      this.baseSpeed = 80 * speedMultiplier;
      this.vx = Math.cos(angle) * this.baseSpeed;
      this.vy = Math.sin(angle) * this.baseSpeed;
    }
    update(dt) {
      this.x += this.vx * dt;
      this.y += this.vy * dt;
      if (this.x < this.radius || this.x > WIDTH - this.radius) this.vx *= -1;
      if (this.y < this.radius || this.y > HEIGHT - this.radius) this.vy *= -1;
    }
    repelFrom(point) {
      const angle = Math.atan2(this.y - point.y, this.x - point.x);
      this.vx = Math.cos(angle) * this.baseSpeed * 2;
      this.vy = Math.sin(angle) * this.baseSpeed * 2;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = colors.drone;
      ctx.shadowBlur = 20;
      ctx.shadowColor = colors.drone;
      ctx.fill();
      ctx.shadowBlur = 0;
      ctx.beginPath();
      ctx.strokeStyle = "rgba(255,255,255,0.25)";
      ctx.lineWidth = 1.5;
      ctx.moveTo(this.x - this.radius - 6, this.y);
      ctx.lineTo(this.x + this.radius + 6, this.y);
      ctx.stroke();
    }
  }

  class Meteor extends Entity {
    constructor() {
      const edges = [
        { x: Math.random() * WIDTH, y: -30, angle: Math.PI / 2 },
        { x: Math.random() * WIDTH, y: HEIGHT + 30, angle: -Math.PI / 2 },
        { x: -30, y: Math.random() * HEIGHT, angle: 0 },
        { x: WIDTH + 30, y: Math.random() * HEIGHT, angle: Math.PI }
      ];
      const spawn = edges[Math.floor(Math.random() * edges.length)];
      super(spawn.x, spawn.y, 22);
      const jitter = (Math.random() - 0.5) * 0.6;
      const angle = spawn.angle + jitter;
      const speed = 220 + Math.random() * 80;
      this.vx = Math.cos(angle) * speed;
      this.vy = Math.sin(angle) * speed;
    }
    update(dt) {
      this.x += this.vx * dt;
      this.y += this.vy * dt;
    }
    isOffscreen() {
      return this.x < -80 || this.x > WIDTH + 80 || this.y < -80 || this.y > HEIGHT + 80;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = colors.meteor;
      ctx.shadowBlur = 25;
      ctx.shadowColor = colors.meteor;
      ctx.fill();
      ctx.shadowBlur = 0;
      ctx.beginPath();
      ctx.strokeStyle = "rgba(255,255,255,0.3)";
      ctx.lineWidth = 2;
      ctx.moveTo(this.x - this.radius - 10, this.y);
      ctx.lineTo(this.x + this.radius + 10, this.y);
      ctx.stroke();
    }
  }

  class PowerUp extends Entity {
      constructor(type) {
        const padding = 50;
        super(
          padding + Math.random() * (WIDTH - padding * 2),
          padding + Math.random() * (HEIGHT - padding * 2),
          14
        );
        this.type = type;
        this.spin = Math.random() * Math.PI * 2;
      }
      update(dt) {
        this.spin += dt * 4;
      }
      draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.spin);
        ctx.beginPath();
        ctx.moveTo(0, -this.radius);
        ctx.lineTo(this.radius, 0);
        ctx.lineTo(0, this.radius);
        ctx.lineTo(-this.radius, 0);
        ctx.closePath();
        const color = this.type === "shield" ? colors.shield : colors.orb;
        ctx.fillStyle = color;
        ctx.shadowBlur = 18;
        ctx.shadowColor = color;
        ctx.fill();
        ctx.shadowBlur = 0;
        ctx.restore();
      }
    }

  class Game {
    constructor() {
      this.difficultyKey = "voyager";
      this.difficulty = DIFFICULTIES[this.difficultyKey];
      this.highscore = Number(localStorage.getItem(LOCAL_KEY) || 0);
      this.input = { up: false, down: false, left: false, right: false };
      this.reset(true);
    }

    reset(full = false) {
      this.player = new Player();
      this.level = 1;
      this.score = 0;
      this.combo = 1;
      this.comboTimer = 0;
      this.shield = this.difficulty.shield;
      this.maxShield = this.difficulty.shield;
      this.paused = false;
      this.orbs = [];
      this.drones = [];
      this.meteors = [];
      this.powerUps = [];
      this.meteorTimer = randRange(...this.difficulty.meteorInterval);
      this.powerupTimer = randRange(...this.difficulty.powerupInterval);
      this.pulseCooldown = 0;
      this.pulseReady = true;
      this.gameOver = false;
      this.logEvent("任务启动，祝你好运！");
      this.spawnWave();
      this.updateUI();
    }

    spawnWave() {
      const orbCount = 4 + this.level;
      const droneBase = 2 + this.level * 0.5;
      const droneCount = Math.min(Math.ceil(droneBase * this.difficulty.droneFactor), 10);
      this.orbs = Array.from({ length: orbCount }, () => new Orb());
      this.drones = Array.from({ length: droneCount }, () => new Drone(this.difficulty.droneFactor));
      this.logEvent(`关卡 ${this.level} 初始化：${orbCount} 个能量球 / ${droneCount} 架无人机。`);
    }

    setDifficulty(mode) {
      if (!DIFFICULTIES[mode]) return;
      this.difficultyKey = mode;
      this.difficulty = DIFFICULTIES[mode];
      buttons.difficulty.forEach((btn) => btn.classList.toggle("active", btn.dataset.mode === mode));
      this.logEvent(`切换至 ${this.difficulty.label} 模式。`);
      this.reset(true);
    }

    logEvent(message) {
      if (!ui.feed) return;
      const li = document.createElement("li");
      const timestamp = new Date().toLocaleTimeString([], { minute: "2-digit", second: "2-digit" });
      li.textContent = `[${timestamp}] ${message}`;
      ui.feed.prepend(li);
      while (ui.feed.children.length > MAX_FEED) {
        ui.feed.removeChild(ui.feed.lastChild);
      }
    }

    updateUI() {
      ui.level.textContent = this.level;
      ui.score.textContent = this.score.toString().padStart(4, "0");
      ui.shield.textContent = this.shield;
      ui.combo.textContent = `x${this.combo}`;
      ui.mode.textContent = this.difficulty.label;
      ui.pulse.textContent = this.pulseReady ? "READY" : `${this.pulseCooldown.toFixed(1)}s`;
      ui.pulse.style.color = this.pulseReady ? "#7af5ff" : "rgba(255,255,255,0.65)";
      ui.boost.textContent = this.player.speedMultiplier > 1 ? "极速推进" : "无";
      ui.meteor.textContent = this.meteors.length ? "流星来袭！" : "空域安全";
      ui.meteor.style.color = this.meteors.length ? colors.meteor : "rgba(199, 216, 255, 0.7)";
    }

    triggerPulse() {
      if (!this.pulseReady || this.paused || this.gameOver) return;
      this.pulseReady = false;
      this.pulseCooldown = this.difficulty.pulseCooldown;
      this.player.triggerPulseVisual();
      this.drones.forEach((drone) => drone.repelFrom(this.player));
      if (this.meteors.length) {
        this.logEvent("护盾脉冲摧毁了来袭流星！");
      }
      this.meteors = [];
      this.logEvent("护盾脉冲已释放。");
      this.updateUI();
    }

    update(dt) {
      if (this.paused || this.gameOver) return;

      this.player.update(dt, this.input);
      this.orbs.forEach((orb) => orb.update(dt));
      this.drones.forEach((drone) => drone.update(dt));
      this.meteors.forEach((meteor) => meteor.update(dt));
      this.powerUps.forEach((power) => power.update(dt));

      this.meteors = this.meteors.filter((meteor) => !meteor.isOffscreen());

      if (this.comboTimer > 0) {
        this.comboTimer -= dt;
        if (this.comboTimer <= 0) {
          this.combo = 1;
        }
      }

      if (!this.pulseReady) {
        this.pulseCooldown -= dt;
        if (this.pulseCooldown <= 0) {
          this.pulseReady = true;
          this.pulseCooldown = 0;
          this.logEvent("护盾脉冲已就绪。");
        }
      }

      this.meteorTimer -= dt;
      if (this.meteorTimer <= 0) {
        this.spawnMeteor();
        this.meteorTimer = randRange(...this.difficulty.meteorInterval);
      }

      this.powerupTimer -= dt;
      if (this.powerupTimer <= 0) {
        this.spawnPowerUp();
        this.powerupTimer = randRange(...this.difficulty.powerupInterval);
      }

      this.checkCollisions();
      this.updateUI();
    }

    spawnMeteor() {
      const meteor = new Meteor();
      this.meteors.push(meteor);
      this.logEvent("流星雨即将经过战区！");
      ui.meteor.textContent = "流星来袭！";
      ui.meteor.style.color = colors.meteor;
    }

    spawnPowerUp() {
      const type = Math.random() < 0.5 ? "shield" : "boost";
      this.powerUps.push(new PowerUp(type));
      this.logEvent(type === "shield" ? "观测到护盾模块。" : "观测到速度模块。");
    }

    checkCollisions() {
      this.orbs = this.orbs.filter((orb) => {
        const collected = distance(this.player, orb) < this.player.radius + orb.radius;
        if (collected) {
          this.combo = this.comboTimer > 0 ? this.combo + 1 : 1;
          this.comboTimer = 2.4;
          this.score += 10 * this.combo;
          if (this.combo > 1) this.logEvent(`连击 x${this.combo}！`);
        }
        return !collected;
      });

      if (!this.orbs.length) {
        this.level += 1;
        this.score += 50;
        this.spawnWave();
      }

      this.drones.forEach((drone) => {
        if (distance(this.player, drone) < this.player.radius + drone.radius) {
          this.absorbDamage(1, "遭遇无人机！");
          this.player = new Player();
        }
      });

      this.meteors.forEach((meteor) => {
        if (distance(this.player, meteor) < this.player.radius + meteor.radius) {
          this.absorbDamage(2, "流星直击！");
          this.player = new Player();
        }
      });

      this.meteors = this.meteors.filter((meteor) => distance(this.player, meteor) >= this.player.radius + meteor.radius);

      this.powerUps = this.powerUps.filter((power) => {
        const hit = distance(this.player, power) < this.player.radius + power.radius;
        if (hit) {
          if (power.type === "shield") {
            if (this.shield < this.maxShield) {
              this.shield += 1;
              this.logEvent("护盾 +1");
            } else {
              this.score += 25;
              this.logEvent("护盾满载，转换为积分。");
            }
          } else {
            this.player.applyBoost(1.8, 4);
            this.logEvent("获取极速推进！");
          }
        }
        return !hit;
      });
    }

    absorbDamage(amount, reason) {
      this.shield -= amount;
      this.logEvent(reason);
      if (this.shield <= 0) {
        this.endRun();
      } else {
        ui.shield.style.color = colors.meteor;
        setTimeout(() => (ui.shield.style.color = ""), 250);
      }
    }

    endRun() {
      this.gameOver = true;
      this.paused = true;
      this.shield = 0;
      this.logEvent("护盾耗尽，任务失败。");
      if (this.score > this.highscore) {
        this.highscore = this.score;
        localStorage.setItem(LOCAL_KEY, this.highscore);
        this.logEvent(`新的本地最高分：${this.score}`);
      }
    }

    draw() {
      ctx.clearRect(0, 0, WIDTH, HEIGHT);
      const gradient = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
      gradient.addColorStop(0, "rgba(97, 242, 255, 0.1)");
      gradient.addColorStop(1, "rgba(255, 141, 244, 0.08)");
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, WIDTH, HEIGHT);

      this.orbs.forEach((orb) => orb.draw());
      this.powerUps.forEach((power) => power.draw());
      this.drones.forEach((drone) => drone.draw());
      this.meteors.forEach((meteor) => meteor.draw());
      this.player.draw();

      if (this.paused && !this.gameOver) {
        this.drawOverlay("暂停中");
      }
      if (this.gameOver) {
        this.drawOverlay("护盾耗尽 · 按 R 重启");
      }

      ctx.textAlign = "right";
      ctx.font = "500 14px 'Inter', sans-serif";
      ctx.fillStyle = "rgba(255,255,255,0.45)";
      ctx.fillText("Space 暂停 · Shift 脉冲 · R 重启", WIDTH - 20, HEIGHT - 20);
    }

    drawOverlay(text) {
      ctx.fillStyle = "rgba(2, 4, 12, 0.65)";
      ctx.fillRect(0, 0, WIDTH, HEIGHT);
      ctx.fillStyle = colors.text;
      ctx.font = "600 36px 'Inter', sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(text, WIDTH / 2, HEIGHT / 2);
    }
  }

  const game = new Game();

  function randRange(min, max) {
    return min + Math.random() * (max - min);
  }

  function distance(a, b) {
    return Math.hypot(a.x - b.x, a.y - b.y);
  }

  function handleKey(e, pressed) {
    const key = e.key.toLowerCase();
    if (["arrowup", "w"].includes(key)) {
      game.input.up = pressed;
      e.preventDefault();
    }
    if (["arrowdown", "s"].includes(key)) {
      game.input.down = pressed;
      e.preventDefault();
    }
    if (["arrowleft", "a"].includes(key)) {
      game.input.left = pressed;
      e.preventDefault();
    }
    if (["arrowright", "d"].includes(key)) {
      game.input.right = pressed;
      e.preventDefault();
    }
    if (pressed) {
      if (key === " ") {
        game.paused = !game.paused;
        e.preventDefault();
      } else if (key === "r") {
        game.reset(true);
      } else if (key === "shift") {
        game.triggerPulse();
      }
    }
  }

  window.addEventListener("keydown", (e) => handleKey(e, true));
  window.addEventListener("keyup", (e) => handleKey(e, false));

  buttons.pause.addEventListener("click", () => (game.paused = true));
  buttons.resume.addEventListener("click", () => {
    if (!game.gameOver) game.paused = false;
  });
  buttons.restart.addEventListener("click", () => game.reset(true));
  buttons.pulse.addEventListener("click", () => game.triggerPulse());
  buttons.difficulty.forEach((btn) =>
    btn.addEventListener("click", () => game.setDifficulty(btn.dataset.mode))
  );

  let last = performance.now();
  function loop(now) {
    const dt = Math.min((now - last) / 1000, 0.033);
    last = now;
    game.update(dt);
    game.draw();
    requestAnimationFrame(loop);
  }

  requestAnimationFrame(loop);
})();