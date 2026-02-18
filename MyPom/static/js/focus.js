const timerDisplay = document.getElementById('time');
const startBtn = document.getElementById('start-btn');
const finaleBtn = document.getElementById('finale-btn');

let timeLeft = 25 * 60;
let interval = null;
let isRunning = false;
let tempoInicial = 25 * 60;

function updateDisplay() {
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

async function finalizarSessao() {
  const wasRunning = isRunning;
  if (isRunning) pauseTimer();

  const salvar = confirm('Deseja finalizar e salvar esta sessão, Benzinho?');

  if (salvar) {
    const tempoEstudado = Math.max(0, tempoInicial - timeLeft);

    try {
      const dataDeHoje = new Date().toISOString().split('T')[0];
      const response = await fetch('/pomo/sessionIn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ duration_seconds: Math.round(tempoEstudado / 60), session_date: dataDeHoje })
      });

      if (response.ok) {
        alert("Sessão salva com sucesso!");
        resetTudo();
      } else {
        alert('Erro ao salvar no servidor.');
      }
    } catch (error) {
      console.error('Erro:', error);
    }
  } else if (wasRunning) {
    startTimer();
  }
}

function resetTudo() {
  clearInterval(interval);
  isRunning = false;
  timeLeft = 25 * 60;
  tempoInicial = 25 * 60;
  clearLocalStorage();
  updateDisplay();
  updateButtonStyle(false);
}

function startTimer() {
  if (!isRunning) {
    isRunning = true;
    const endTime = new Date().getTime() + (timeLeft * 1000);
    localStorage.setItem('pomoEndTime', endTime);
    localStorage.setItem('pomoIsRunning', 'true');
    localStorage.setItem('pomoTempoInicial', tempoInicial);

    startInterval();
    updateButtonStyle(true);
  } else {
    pauseTimer();
  }
}

function pauseTimer() {
  isRunning = false;
  clearInterval(interval);
  localStorage.setItem('pomoIsRunning', 'false');
  localStorage.setItem('pomoTimeLeft', timeLeft);
  updateButtonStyle(false);
}

function startInterval() {
  if (interval) clearInterval(interval);
  interval = setInterval(() => {
    if (timeLeft > 0) {
      timeLeft--;
      updateDisplay();
    } else {
      clearInterval(interval);
      resetTudo();
      alert('Fim do ciclo!');
    }
  }, 1000);
}

function updateButtonStyle(running) {
  if (running) {
    startBtn.innerHTML = 'Pausar';
    startBtn.style.background = "#f1c40f";
    startBtn.style.color = "black";
  } else {
    startBtn.innerHTML = 'Iniciar';
    startBtn.style.background = "#2ecc71";
    startBtn.style.color = "white";
  }
}

function alterarTempo(min) {
  let savedEndTime = localStorage.getItem("pomoEndTime");

  if (!savedEndTime) {
    let novoTempo = timeLeft + (min * 60);
    if (novoTempo > 0) {
      timeLeft = novoTempo;
      updateDisplay();
    }
    return;
  }

  let addMiliSegunds = min * 60 * 1000;
  let newEndTime = parseInt(savedEndTime) + addMiliSegunds;

  if (newEndTime > new Date().getTime()) {
    localStorage.setItem('pomoEndTime', newEndTime);

    timeLeft = Math.round((newEndTime - new Date().getTime()) / 1000);
    updateDisplay();
  } else {
    console.error('ERROR: o tempo resultante seria negativo.')
  }


}

function clearLocalStorage() {
  localStorage.removeItem('pomoEndTime');
  localStorage.removeItem('pomoIsRunning');
  localStorage.removeItem('pomoTimeLeft');
  localStorage.removeItem('pomoTempoInicial');
}

function recoverState() {
  const savedEndTime = localStorage.getItem('pomoEndTime');
  const savedIsRunning = localStorage.getItem('pomoIsRunning') === 'true';
  const savedTimeLeft = localStorage.getItem('pomoTimeLeft');
  const savedTempoInicial = localStorage.getItem('pomoTempoInicial');

  if (savedTempoInicial) tempoInicial = parseInt(savedTempoInicial);

  if (savedIsRunning && savedEndTime) {
    const remaining = Math.round((savedEndTime - new Date().getTime()) / 1000);
    if (remaining > 0) {
      timeLeft = remaining;
      isRunning = true;
      startInterval();
      updateButtonStyle(true);
    } else {
      resetTudo();
    }
  } else if (savedTimeLeft) {
    timeLeft = parseInt(savedTimeLeft);
    updateDisplay();
  }
}

document.addEventListener('DOMContentLoaded', recoverState);
startBtn.addEventListener('click', startTimer);
finaleBtn.addEventListener('click', finalizarSessao);
