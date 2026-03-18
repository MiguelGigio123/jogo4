<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Square Jump</title>
<style>
body { margin:0; font-family:Arial; text-align:center; background:#111; color:#fff; }
canvas { background:#222; display:block; margin:0 auto; }
</style>
</head>
<body>
<h1>Square Jump</h1>
<canvas id="gameCanvas" width="800" height="600"></canvas>
<p>Setas ← → para mover | ↑ para pular</p>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let keys = {};
document.addEventListener("keydown", e => keys[e.key] = true);
document.addEventListener("keyup", e => keys[e.key] = false);

let player = { x:50, y:500, w:30, h:30, vy:0, grounded:false, hits:0 };
let gravity = 0.8;

let level = 1;
let enemies = [];
let obstacles = [];
let boss = null;

function resetLevel(){
    player.x = 50;
    player.y = 500;
    player.vy = 0;
    enemies = [];
    obstacles = [];
    boss = null;

    if(level < 10){
        for(let i=0;i<level;i++){
            enemies.push({x:300+i*120,y:500,w:30,h:30,speed:2+level});
        }
        for(let i=0;i<level;i++){
            obstacles.push({x:200+i*150,y:520,w:40,h:20});
        }
    } else {
        boss = {x:650,y:450,w:80,h:80,shots:[]};
    }
}

function rectsCollide(a,b){
    return a.x < b.x + b.w &&
           a.x + a.w > b.x &&
           a.y < b.y + b.h &&
           a.y + a.h > b.y;
}

function update(){
    // movimento
    if(keys["ArrowLeft"]) player.x -= 5;
    if(keys["ArrowRight"]) player.x += 5;

    if(keys["ArrowUp"] && player.grounded){
        player.vy = -15;
        player.grounded = false;
    }

    player.vy += gravity;
    player.y += player.vy;

    if(player.y >= 500){
        player.y = 500;
        player.vy = 0;
        player.grounded = true;
    }

    // obstáculos
    obstacles.forEach(o => {
        if(rectsCollide(player,o)){
            player.y = o.y - player.h;
            player.vy = 0;
            player.grounded = true;
        }
    });

    // inimigos
    enemies.forEach(e => {
        e.x -= e.speed;
        if(e.x < -50) e.x = 800;
        if(rectsCollide(player,e)) resetLevel();
    });

    // boss
    if(boss){
        if(Math.random() < 0.03){
            boss.shots.push({x:boss.x,y:boss.y+40,size:20});
        }

        boss.shots.forEach(s => {
            s.x -= 6;
            if(rectsCollide(player,{x:s.x,y:s.y,w:s.size,h:s.size})){
                resetLevel();
            }
        });

        if(rectsCollide(player,boss)){
            player.hits++;
            player.x = 50;
        }

        if(player.hits >= 10){
            alert("Você venceu o jogo!");
            level = 1;
            player.hits = 0;
            resetLevel();
        }
    }

    // avançar fase
    if(!boss && player.x > 750){
        level++;
        resetLevel();
    }
}

function draw(){
    ctx.clearRect(0,0,800,600);

    // jogador
    ctx.fillStyle = "lime";
    ctx.fillRect(player.x,player.y,player.w,player.h);

    // obstáculos
    ctx.fillStyle = "gray";
    obstacles.forEach(o => ctx.fillRect(o.x,o.y,o.w,o.h));

    // inimigos
    ctx.fillStyle = "red";
    enemies.forEach(e => ctx.fillRect(e.x,e.y,e.w,e.h));

    // boss
    if(boss){
        ctx.fillStyle = "purple";
        ctx.fillRect(boss.x,boss.y,boss.w,boss.h);

        ctx.fillStyle = "yellow";
        boss.shots.forEach(s => {
            ctx.beginPath();
            ctx.moveTo(s.x, s.y);
            ctx.lineTo(s.x+s.size, s.y+s.size/2);
            ctx.lineTo(s.x, s.y+s.size);
            ctx.fill();
        });
    }

    ctx.fillStyle = "white";
    ctx.fillText("Fase: " + level, 10, 20);
    if(boss) ctx.fillText("Hits no Boss: " + player.hits + "/10", 10, 40);
}

function gameLoop(){
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

resetLevel();
gameLoop();
</script>
</body>
</html>
