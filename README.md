---


---

<h1 id="tabla-postgre">Tabla Postgre</h1>
<p><em>versión Beta</em></p>
<p>El módulo contiene la <a href="https://es.wikipedia.org/wiki/Clase_%28inform%C3%A1tica%29">clase</a> <em>TablaPostgre</em>. Su objetivo es brindar a los desarrolladores la capacidad de  interactuar con tablas de datos a manera de objetos, permitiendo aplicar técnicas de modularidad, encapsulamiento, herencia y polimorfismo para facilitar el desarrollo de sus aplicaciones con bases de datos PostgreSQL.</p>
<p>Para el buen uso de las instancias creadas a partir de <em>TablaPostgre</em> debe tomar en cuenta lo siguiente:</p>
<ul>
<li>
<p>▶️Ante cualquier interacción con los métodos de la clase debe tener presente la sintaxis PostgreSQL, para consultar más información al respecto visite el sitio oficial: <a href="https://www.postgresql.org/docs">https://www.postgresql.org/docs</a></p>
</li>
<li>
<p>▶️Usted debe proporcionar las credenciales de su base de datos PostgreSQL mediante la modificación manual del código (preferiblemente utilizar llamado de variables globales). La seguridad de sus credenciales dependerá de la forma en la que usted realice esta gestión. Las credenciales que vienen por defecto son únicamente para efectos de ejemplo y pueden no estar vigentes en este momento.</p>
</li>
</ul>
<font color="red">*<strong>Nota</strong>: Usted es responsable de gestionar las credenciales según el nivel de seguridad que necesite. La siguiente imagen debe ser tomada únicamente como ejemplo y no como instrucciones de uso.</font><br>
<h3 id="🤖instanciación">🤖Instanciación</h3>
<p>El método constructor imprimirá detalles sobre la tabla creada.<br>
Las siguientes columnas se construyen automáticamente para cada instancia:</p>
<ol>
<li>llave: valor único necesario para ejecución de algunos de los métodos, y relaciones entre tablas.</li>
<li>usuario_act: registra el nombre del usuario que ejecuta algún método.</li>
<li>fecha_act: registra la fecha en la que fue ejecutado un método.</li>
</ol>
<h3 id="🤖ejecución-de-métodos">🤖Ejecución de métodos</h3>
<p>Cada método devuelve un detalle sobre su ejecución, lo cual permite llevar una bitácora de la manipulación de la tabla.</p>
<p>Para conocer detalles sobre la totalidad de los métodos consulte los <em>docstrings</em> del módulo.<br>
---
<p><em>tablapostgre</em> irá siendo mejorado y adaptado a diferentes versiones de Python y otros lenguajes con el paso del tiempo.</p>
---
<p>Puedes apoyar el trabajo realizando una donación voluntaria mediante el servicio Paypal haciendo click en el siguiente enlace:</p>
<p><a href="https://paypal.me/Feoli"><img src="https://lh3.googleusercontent.com/XPKrFY-av-IOwcY1a8ff91evfQUfxPdlk0fS4WtHitOyyixqvYifrTUZYAU4eCKRICWHvBW5wqE_Pw=s235" alt="enter image description here"></a></p>

