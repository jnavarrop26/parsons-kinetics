<div align="center">
  <img src="https://img1.wsimg.com/isteam/ip/23944649-2ef8-4147-a4b4-6f57c00c6115/blob-b4af893.png/:/rs=w:828,h:225,cg=true,m/cr=w:828,h:225/qt=q:95" alt="parsons kinetics logo">
</div>


Este proyecto es el **MVP** (*Minimo Producto Viable*) de la aplicación beta de **Parsons Kinetics**, que permite a los usuarios estimar la producción de energía eólica en función de las coordenadas geográficas proporcionadas.

## **Descripción**

La aplicación permite a los usuarios ingresar coordenadas de latitud y longitud junto con un filtro de fecha de inicio y fecha final para estimar la producción de energía eólica en esa ubicación. La interfaz de usuario está construida utilizando **HTML5** y **CCS3**, y está diseñada para ser intuitiva y fácil de usar.

## **Características**

- **Estimación de Producción**: Los usuarios pueden ingresar coordenadas de latitud y longitud junto con un filtro de fecha de inicio y fecha final para estimar la producción de energía eólica en esa ubicación.

- **Visualización de Datos**: Los usuarios pueden ver la producción estimada de energía eólica en un gráfico de barras.

- **Historial de Consultas**: Los usuarios pueden ver un historial de las consultas realizadas, incluidas las coordenadas de latitud y longitud, la fecha de inicio y la fecha final.

## **Herramientas Utilizadas**

![GitHub Badge](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=fff&style=flat)
![Python Badge](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![DJANGO Badge](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-%23E34F26.svg?&style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-%231572B6.svg?&style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-%23F7DF1E.svg?&style=flat&logo=javascript&logoColor=white)
![Open Meteo API](https://img.shields.io/badge/Open%20Meteo%20API-%23FFA500.svg?&style=flat&logo=Open%20Meteo%20API&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?&style=flat&logo=sqlite&logoColor=white)

## **Librerias** 

![NumPy](https://img.shields.io/badge/NumPy-%23013243.svg?&style=flat&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-%23150458.svg?&style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23E34F26.svg?&style=flat&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-%231572B6.svg?&style=flat&logo=seaborn&logoColor=white)
![OpenMeteo Request](https://img.shields.io/badge/OpenMeteo%20Request-%23F7DF1E.svg?&style=flat&logo=OpenMeteo%20Request&logoColor=white)
![Base64](https://img.shields.io/badge/Base64-%23FFA500.svg?&style=flat&logo=Base64&logoColor=white)


## Guía para Levantar una Aplicación de Django

### **Requisitos Previos**

- Python 3.x
- pip (gestor de paquetes de Python)
- Virtualenv (opcional pero recomendado)

# **Pasos para Levantar la Aplicación**

## **Requisitos Previos**

- Python 3.x
- pip (gestor de paquetes de Python)
- Virtualenv (opcional pero recomendado)

## **Pasos para Levantar la Aplicación**
+ **Crear un entorno virtual**
```bash
python -m venv venv
```

> [!IMPORTANT]  
> Nosotros proporcionamos el entorno virtual en el proyecto, por lo que no es necesario crear uno.

+ **Activar el entorno virtual (Windows)**
```
venv\Scripts\activate
```

+ **Activar el entorno virtual (MacOS/Linux)**
``` 
source venv/bin/activate
```

Posteriormente desde la terminal, navegar hasta el directorio del proyecto desde encontrarse en el path ```parsons-kinetics-mvp``` y ejecutar el siguiente comando:

```bash
python manage.py runserver
```	
**Acceder a la aplicación**

Abre tu navegador y ve a  ``` http://localhost:8000/ ``` para ver tu aplicación en funcionamiento.


## **Autores**

Somos estudiantes del pregrado de **Ingeniería de Sistemas** de la **Universidad Central**.

**Jose Antonio Navarro Parody**

  [![LinkedIn](https://img.shields.io/badge/LinkedIn-Jose_Navarro-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=101010)](https://www.linkedin.com/in/jose-navarro-b0361b23b/)
  [![GitHub](https://img.shields.io/badge/GitHub-jnavarrop26-181717?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://github.com/jnavarrop26)
  [![Gmail](https://img.shields.io/badge/Gmail-jnavarrop@ucentral.edu.co-D14836?style=for-the-badge&logo=gmail&logoColor=white&labelColor=101010)](mailto:jnavarrop@ucentral.edu.co)

**Juan Esteban Alba Rodriguez**

 [![Gmail](https://img.shields.io/badge/Gmail-jalbar@ucentral.edu.co-D14836?style=for-the-badge&logo=gmail&logoColor=white&labelColor=101010)](mailto:jalbar@ucentral.edu.co)

**David Martinez**

[![Gmail](https://img.shields.io/badge/Gmail-dmartinezg8@ucentral.edu.co-D14836?style=for-the-badge&logo=gmail&logoColor=white&labelColor=101010)](mailto:dmartinezg8@ucentral.edu.co)