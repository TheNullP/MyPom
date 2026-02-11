const total_hoje = document.getElementById("total_hoje");
const total_semanal = document.getElementById('total_semana');


document.addEventListener('DOMContentLoaded', async () => {
  function sum_duration(mints) {
    let hour = mints / 60 | 0;
    let mn = mints % 60;


    return `${String(hour).padStart(2, '0')}:${String(mn).padStart(2, '0')}`

  }

  try {
    const response_dia = await fetch('/pomo/dailysession');

    if (!response_dia.ok) {
      throw new Error('ERROR: Sem dados do dia.');
    }

    const data = await response_dia.json();


    total_hoje.innerText = sum_duration(data[0].total_seconds)

  } catch (error) {
    console.error(error);
  }
  try {
    const response_semana = await fetch('/pomo/weekSession');

    if (!response_semana.ok) {
      throw new Error('ERROR: Sem dados da semana.');
    }

    const data_semana = await response_semana.json();



    total_semanal.innerText = sum_duration(data_semana[0]);

  } catch (error) {
    console.error(error);
  }
});
