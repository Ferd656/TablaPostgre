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
<p>▶️Usted debe proporcionar las credenciales de su base de datos PostgreSQL mediante la modificación manual del código. La seguridad de sus credenciales dependerá de la forma en la que usted realice esta gestión. Las credenciales que vienen por defecto son únicamente para efectos de ejemplo y pueden no estar vigentes en este momento.</p>
</li>
</ul>
<h2 id="ejemplos-de-uso">Ejemplos de uso</h2>
<h3 id="🤖definición-de-credenciales">🤖Definición de credenciales</h3>
<p>Tenemos una base de datos PostgreSQL en la web con las siguientes credenciales:<br>
<img src="https://lh3.googleusercontent.com/I8l7bEvh9SRH61ZHmEczITbZgg6AOZVtRlPKu3FaVDLIPh3PLZCcc6ISdtm9o2YGI6gP37YCTG31ig" alt="enter image description here"></p>
<p>Se añaden las credenciales al código:<br>
<font color="red">*<strong>Nota</strong>: Usted es responsable de gestionar las credenciales según el nivel de seguridad que necesite. La siguiente imagen debe ser tomada únicamente como ejemplo y no como instrucciones de uso.</font><br>
<img src="https://lh3.googleusercontent.com/otDVnXILBbDtNwdAe9JTn1TTdcMzENQxlZ7kMsF6Q7U2ntCZp5o8XDCdBDBrSb5VmSqrEJTIiNcpWg" alt="enter image description here"></p>
<h3 id="🤖instanciación">🤖Instanciación</h3>
<p>El método constructor imprimirá detalles sobre la tabla creada.<br>
Las siguientes columnas se construyen automáticamente para cada instancia:</p>
<ol>
<li>llave: valor único necesario para ejecución de algunos de los métodos, y relaciones entre tablas.</li>
<li>usuario_act: registra el nombre del usuario que ejecuta algún método.</li>
<li>fecha_act: registra la fecha en la que fue ejecutado un método.</li>
</ol>
<p><img src="https://lh3.googleusercontent.com/LGc0Qv_uAD_Nyl45Yee34tyIdItV7X0SdF0ZZIrNTaalWXTFotLQB3AM2KK7dmJvoul67InTgDnyLg" alt="enter image description here"></p>
<h3 id="🤖ejecución-de-métodos">🤖Ejecución de métodos</h3>
<p>A continuación se ejemplifica el funcionamiento de algunos de los métodos de la clase <em>TablaPostgre</em>:</p>
<p>Cada método devuelve un detalle sobre su ejecución, lo cual permite llevar una bitácora de la manipulación de la tabla.</p>
<p>Para conocer detalles sobre la totalidad de los métodos consulte los <em>docstrings</em> del módulo.<br>
Ejemplo:<br>
<img src="https://lh3.googleusercontent.com/O3C47ixFRlZvNVJuOwvaVSFAyANlujcx7kBZoHe8oUPOCz-ei2Y-1GjqRJen1aK4mBeZofr1JlL-HA" alt="enter image description here"></p>
<h4 id="💡agregar-registros">💡Agregar registros</h4>
<p><img src="https://lh3.googleusercontent.com/kt2n5YiqMDKiltRxMXrwZX0Iwa6klSr90clGZ0J5C_7NhLAhg1s7NuT16pGhVYvpfS8Gy-S2Bq3lDQ" alt="enter image description here"></p>
<h4 id="💡actualizar-registros">💡Actualizar registros</h4>
<p><img src="https://lh3.googleusercontent.com/b0NVswzZFSLVS0TuabWyJgq6KCNsj1no4icv4k2xnCNHWuEPMOh6VIAGiSqIWCKCdCmSN-C-xtN2oA" alt="enter image description here"></p>
<h4 id="💡eliminar-registros">💡Eliminar registros</h4>
<p><img src="https://lh3.googleusercontent.com/OlE2blxJNBqGQo_UiXmVbYU8AFRBa-xMNhEdy9WjMbtTNIXrjOqj2Fle_NdfLoGvcCQvBNoVAjK5sg" alt="enter image description here"></p>
<h4 id="💡consultar-columnas">💡Consultar columnas</h4>
<p><img src="https://lh3.googleusercontent.com/zosBkOAJBfNKjf_nDNOuz1Sp95bfXX6FWjSk3-g5f8Ll1YeuP31Z5vlfJd_jTXlCgQcUT_wvU02bKw" alt="enter image description here"></p>
<h4 id="💡ejecutar-sentencia-sql-personalizada">💡Ejecutar sentencia SQL personalizada</h4>
<p><img src="https://lh3.googleusercontent.com/MVPihE-q7ZMtqGWLryZJG3TqkAxwM7YFmj23bFjZNo9gV6SKEC1_OgVdVQrSxyF8XgtB4EjZWYRTFw" alt="enter image description here"></p>
<h4 id="💡exportar-datos-como-dataframe-de-pandas">💡Exportar datos como Dataframe de Pandas</h4>
<h2 id="section"><img src="https://lh3.googleusercontent.com/3EFsV0AOL-uBM55Rv_IwBExF9tdTeICUaC6hOjA8PJ-AFXGuBP9qZ_JiG8td6orqla81XKit-7_SVQ" alt="enter image description here"></h2>
<p><em>tablapostgre</em> irá siendo mejorado y adaptado a diferentes versiones de Python y otros lenguajes con el paso del tiempo.</p>
<p>Puedes apoyar el trabajo realizando una donación voluntaria mediante el servicio Paypal haciendo click en el siguiente enlace:</p>
<p><a href="https://paypal.me/Feoli"><img src="https://lh3.googleusercontent.com/XPKrFY-av-IOwcY1a8ff91evfQUfxPdlk0fS4WtHitOyyixqvYifrTUZYAU4eCKRICWHvBW5wqE_Pw=s235" alt="enter image description here"></a></p>

