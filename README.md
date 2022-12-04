# Windy Golfing
This project demonstrates a data-intensive RESTful web application with an asynchronous, distributed computation backend, built around a Monte Carlo simulation that seeks to quantify agent skill at hitting a target within a dynamical system. In this scenario, the agents are golfers and the dynamical system is the wind whose behaviour follows varying models to set the golfing environment. These include a perfectly calm day (no wind), wind that oscillates predictably, and wind whose speed and direction evolves chaotically as modeled by a Lorenz attractor, which is a nod to Lorenz' invention of this famous model for atmospheric convection. (https://en.wikipedia.org/wiki/Lorenz_system).

## The stack
* **Database**: *Postgres* (as the RDB), *Azure Blob Storage* (to hold sim data), *RabbitMQ* (task broker), *Redis* (task result backend & cacheing)
* **Monte Carlo simulation**: built with *numpy* and *pandas* in a *Jupyter* sandbox 
* **Backend**: *Django Rest Framework* and *Celery* (for parallel computing)
* **Frontend**: *Vue.js* with *TailwindCSS*
* **Visualization**: *Highcharts*
