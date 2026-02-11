const elements = document.querySelectorAll('.pc_stats')





async function update_stats(){

    const response = await fetch("/api/system-stats/");

    const data = await response.json()
    

    elements[0].textContent = `Zuzycie PROCESORA ${data['CPU Usage']}`
    elements[1].textContent = `Zuzycie RAMU ${data['RAM Usage']}`
}


setInterval(update_stats, 1000)
