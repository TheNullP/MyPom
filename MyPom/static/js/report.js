const total_day = document.getElementById("total_hoje");
const total_week = document.getElementById('total_semana');
const total_month = document.getElementById('total_mes');
const indicador = document.getElementById('indicador');


document.addEventListener('DOMContentLoaded', async () => {
  function sum_duration(mints) {
    let hour = mints / 60 | 0;
    let mn = mints % 60;


    return `${String(hour).padStart(2, '0')}:${String(mn).padStart(2, '0')}`

  }

  try {
    const response = await fetch('/pomo/dailysession');

    if (!response.ok) {
      throw new Error('ERROR: Sem dados do dia.');
    }

    const data = await response.json();


    total_day.innerText = sum_duration(data[0].total_seconds);

  } catch (error) {
    console.error(error);
  }
  try {
    const response = await fetch('/pomo/weekSession');

    if (!response.ok) {
      throw new Error('ERROR: Sem dados da semana.');
    }

    const data = await response.json();


    total_week.innerText = sum_duration(data[0]);

  } catch (error) {
    console.error(error);
  }
  try {
    const response = await fetch('/pomo/monthSession')

    if (!response.ok) {
      throw new Error('Error: Sem dados do mês.');
    }

    const data = await response.json();

    total_month.innerText = sum_duration(data.total_month_duration_minuts);

  } catch (error) {
    console.error(error);

  }
  try {
    const response = await fetch('/pomo/differenceInDays');

    if (!response.ok) {
      throw new Error('Error: Sem dados para comparação.');
    }
    const data = await response.json();

    if (data.difference > 0) {

      indicador.innerText = `Hoje você estudou ${data.difference} minutos a mais que ontem.`
      return;
    } else if (data.difference < 0) {
      indicador.innerText = `Hoje você estudou ${data.difference * (-1)} minutos a menos que ontem.`
      indicador.style.color = "red"
    }


  } catch (error) {
    throw new Error('Error: sem dados para comparação.')

  }

});
