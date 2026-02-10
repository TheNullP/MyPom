const total_hoje = document.getElementById("total_hoje");
const total_semanal = document.getElementById('total_semana');


document.addEventListener('DOMContentLoaded', async () => {

  try {
    const response_dia = await fetch('/pomo/dailysession');
    const response_semana = await fetch('/pomo/weekSession', { method: "GET" });

    if (!response_dia.ok) {
      throw new Error('ERROR: Sem dados do dia.');
    }
    if (!response_semana.ok) {
      throw new Error('ERROR: Sem dados da semana.');
    }

    const data = await response_dia.json();
    const data_semana = await response_semana.json();


    total_hoje.innerText = `${data[0].total_seconds}`;
    total_semanal.innerText = data_semana[0].duration;

  } catch (error) {
    console.error(error);
  }
});
