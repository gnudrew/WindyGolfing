# Windy Golfing
This project demonstrates a data-intensive RESTful web application with an asynchronous, distributed computation backend, built around a Monte Carlo simulation to measure agent skill at acheiving a target in a dynamical system. In this case the agents are golfers and the dynamical system is wind with modeled behaviour including a perfectly calm day, an oscillatory wind behaviour, and (more realistically) chaotic wind behaciour modeled by a Lorenz attractor, who famously first described atmospheric convection.

## The stack
* **Database**: *Postgres* (as the RDB), *Azure Blob Storage* (to hold sim data), *RabbitMQ* (task broker), *Redis* (task result backend & cacheing)
* **Monte Carlo simulation**: built with *numpy* and *pandas* in a *Jupyter* sandbox 
* **Backend**: *Django Rest Framework* and *Celery* (for parallel computing)
* **Frontend**: *Vue.js* with *TailwindCSS*
* **Visualization**: *Highcharts*
