from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

# 1. Inicializar la sesión de Spark
spark = SparkSession.builder \
    .appName("UNAD_BigData_Batch") \
    .getOrCreate()

# Configurar el nivel de log a WARN para evitar exceso de mensajes INFO en la consola
spark.sparkContext.setLogLevel("WARN")

print("\n=== PASO 1: CARGA DEL CONJUNTO DE DATOS ===")
# Carga del dataset propio e inferencia automática del esquema de los datos
df = spark.read.csv("datos_contaminacion.csv", header=True, inferSchema=True)
print("Muestra de las primeras 5 filas del dataset original:")
df.show(5)

print("\n=== PASO 2: OPERACIONES DE LIMPIEZA ===")
# Eliminación de registros con valores nulos o vacíos en la variable crítica PM2.5
df_limpio = df.dropna(subset=["PM25"])
print(f"Total registros originales: {df.count()} | Total registros limpios: {df_limpio.count()}")

print("\n=== PASO 3: ANÁLISIS EXPLORATORIO DE DATOS (EDA) ===")
# Generación de estadísticas descriptivas esenciales para las variables numéricas ambientales
df_limpio.select("PM25", "CO2", "Temperatura").describe().show()

print("\n=== PASO 4: TRANSFORMACIÓN Y AGRUPACIÓN POR CIUDAD ===")
# Agrupación por ciudad para calcular el promedio de contaminación PM2.5 ordenado de mayor a menor
df_resultado = df_limpio.groupBy("Ciudad") \
    .agg(avg("PM25").alias("Promedio_PM25")) \
    .orderBy("Promedio_PM25", ascending=False)

print("Resultado consolidado del análisis por lotes:")
df_resultado.show()

print("=========================================================")
print("¡Procesamiento Batch en Spark completado con éxito!")
print("=========================================================")

# Cerrar la sesión de Spark de forma segura
spark.stop()
