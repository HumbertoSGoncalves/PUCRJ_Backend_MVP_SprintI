# MVP Backend - Virtual Wine Cellar

This project meets the requirements for the delivery of the MVP for **Sprint I: Basic Full Stack Development** of the Postgraduate Program in Software Engineering at PUC RIO.
(https://especializacao.ccec.puc-rio.br/especializacao/engenharia-de-software)

The goal is to use the content taught during the classes to create a single-page application with both the front and back end. A virtual Wine Cellar was designed to make this possible, where wines can be added, consulted, or deleted.

More specifically, the **backend of the MVP** will be explored for the codes provided here.

---
## How to execute 

- Update all the listed Python libraries according to the `requirements.txt` file. In other words, the installation can be executed in the chosen environment using the command:
```
pip install -r requirements.txt;
```

- To run the API: 
```
flask run --host 0.0.0.0 --port 5000
```

- It is recommended to use the following command when in development mode:
```
flask run --host 0.0.0.0 --port 5000 --reload
```
By doing this, the server restarts automatically after changes to the source code are made.

Access [http://localhost:5000/#/](http://localhost:5000/#/) in your preferred browser to check the running API.
Afterwards, you can test any API routes you want to manage your virtual wine cellar. Each route is appropriately described in the accessible documentation.
