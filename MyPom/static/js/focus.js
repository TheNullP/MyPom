const timerDisplay = document.getElementById('time');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const finaleBtn = document.getElementById('finale-btn');

let timeLeft = 25 * 60;
let timerId = null;
let tempoInicial = 25 * 60;

function updateDisplay() {
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

function alterarTempo(minutos) {
  if (timerId !== null) return;

  let novoTempo = timeLeft + (minutos * 60);

  if (novoTempo > 0) {
    timeLeft = novoTempo;
    tempoInicial = novoTempo;
    updateDisplay();
  }
}

async function finalizarSessao() {
  clearInterval(timerId);
  timerId = null;

  const salvar = confirm('Deseja finalzar sessão?');
  if (salvar) {
    tempoSessao = tempoInicial - timeLeft;

    try {
      const dataDeHoje = new Date().toISOString().split('T')[0];
      

      const response = await fetch('/pomo/sessionIn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ duration_minutes: tempoSessao, session_date: dataDeHoje,})
      });

      if (response.ok) {
        alert("Sessão salva com sucesso.")
      } else {
        alert('Erro ao salvar sessão no backEnd.')
      }

    } catch (error) {
      console.error('Errp na requisição: ', error);
    }
  }
}

function startTimer() {
  if (timerId !== null) return;

  timerId = setInterval(() => {
    if (timeLeft > 0) {
      timeLeft--;
      updateDisplay();
    } else {
      clearInterval(timerId);
      alert('Hora do descanso.');
    }
  }, 1000);
}

function pauseTimer() {
  clearInterval(timerId);
  timerId = null;
}

function finaleTimer() {
  finalizarSessao();
  // pauseTimer();
  timeLeft = 25 * 60;
  updateDisplay();
}

startBtn.addEventListener('click', startTimer);
pauseBtn.addEventListener('click', pauseTimer);
finaleBtn.addEventListener('click', finaleTimer);
