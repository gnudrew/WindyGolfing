# Windy Golfing
This project demonstrates a data-intensive RESTful web application with an asynchronous, distributed computation backend, built around a Monte Carlo simulation that seeks to quantify agent skill at hitting a target within a dynamical system. In this case, the agents are golfers and the dynamical system is wind whose behaviour is modeled by a few different systems, including a perfectly calm day, wind that oscillates predictably, and (more realistically) wind whose speed and direction varies chaotically modeled by a Lorenz attractor, as an a nod to its invention as a model for atmospheric convection (https://en.wikipedia.org/wiki/Lorenz_system).

## The stack
* **Database**: *Postgres* (as the RDB), *Azure Blob Storage* (to hold sim data), *RabbitMQ* (task broker), *Redis* (task result backend & cacheing)
* **Monte Carlo simulation**: built with *numpy* and *pandas* in a *Jupyter* sandbox 
* **Backend**: *Django Rest Framework* and *Celery* (for parallel computing)
* **Frontend**: *Vue.js* with *TailwindCSS*
* **Visualization**: *Highcharts*
