import csv
import io
import plotly.graph_objs as go
from plotly.offline import plot
import numpy as np

from django.shortcuts import render
from .forms import CSVUploadForm
from .models import Producto

def graficas(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_csv = request.FILES['archivo_csv']
            datos = archivo_csv.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(datos))

            productos = {}
            for row in reader:
                producto = row['producto']
                ano = int(row['ano'])
                mes = row['mes']
                precio = float(row['precio'])
                moneda = row['moneda']

                if producto not in productos:
                    productos[producto] = {}

                if ano not in productos[producto]:
                    productos[producto][ano] = []

                productos[producto][ano].append(precio)

                Producto.objects.update_or_create(
                    producto=producto,
                    ano=ano,
                    mes=mes,
                    defaults={'precio': precio, 'moneda': moneda}
                )

            # Generar la primera gráfica
            nombres_productos = list(productos.keys())
            precios_productos = [list(productos[producto].values()) for producto in nombres_productos]

            data = []
            for i, producto in enumerate(nombres_productos):
                x_labels = [f'{ano}' for ano in productos[producto].keys()]
                data.append(go.Bar(x=x_labels, y=precios_productos[i], name=producto))

            layout = go.Layout(
                title='Gráfico de Inflación de Productos',
                xaxis=dict(title='Año'),
                yaxis=dict(title='Precio'),
                bargap=0.2,
                hovermode='closest'
            )

            fig = go.Figure(data=data, layout=layout)
            plot_div = plot(fig, output_type='div')

            # Cálculo de la tasa de inflación anual para cada producto
            tasa_inflacion_productos = {}
            for producto in productos:
                tasa_inflacion = []
                for ano, precios in productos[producto].items():
                    tasa = ((precios[-1] - precios[0]) / precios[0]) * 100
                    tasa_inflacion.append(tasa)
                tasa_inflacion_productos[producto] = tasa_inflacion

            # Generar la segunda gráfica
            data2 = []
            for i, producto in enumerate(nombres_productos):
                x_labels = [f'{ano}' for ano in productos[producto].keys()]
                data2.append(go.Bar(x=x_labels, y=tasa_inflacion_productos[producto], name=producto))

            layout2 = go.Layout(
                title='Tasa de Inflación Anual',
                xaxis=dict(title='Año'),
                yaxis=dict(title='Tasa de Inflación (%)'),
                bargap=0.2,
                hovermode='closest'
            )

            fig2 = go.Figure(data=data2, layout=layout2)
            plot_div2 = plot(fig2, output_type='div')

            # Cálculo de las proyecciones de costos futuros
            inflacion_actual = [tasa_inflacion[-1] for tasa_inflacion in tasa_inflacion_productos.values()]
            periodo_proyeccion = 5

            proyecciones_costos = {}
            for producto in productos:
                precios_actuales = list(productos[producto].values())[-1]
                proyeccion = [precio * np.power((1 + inflacion/100), i+1) for i, precio, inflacion in zip(range(periodo_proyeccion), precios_actuales, inflacion_actual)]
                proyecciones_costos[producto] = proyeccion

            # Generar la tercera gráfica (Proyecciones de costos futuros)
            data3 = []
            for i, producto in enumerate(nombres_productos):
                x_labels = [f'{ano}' for ano in productos[producto].keys()]
                data3.append(go.Scatter(x=x_labels, y=proyecciones_costos[producto], name=producto, text=proyecciones_costos[producto], mode='lines+markers', hovertemplate='Precio: %{text:.2f}'))

            layout3 = go.Layout(
                title='Proyecciones de Costos Futuros',
                xaxis=dict(title='Año'),
                yaxis=dict(title='Costo'),
                hovermode='closest'
            )

            fig3 = go.Figure(data=data3, layout=layout3)
            plot_div3 = plot(fig3, output_type='div')

            # Cálculo de la tasa de rendimiento ajustada por inflación para cada producto
            tasa_rendimiento_productos = {}
            for producto in productos:
                precios = list(productos[producto].values())[-1]
                inflacion = tasa_inflacion_productos[producto]
                rendimiento_ajustado = [((precio / infl) - 1) * 100 for precio, infl in zip(precios, inflacion)]
                tasa_rendimiento_productos[producto] = rendimiento_ajustado

            # Generar la cuarta gráfica (Comparación de rendimientos de inversión)
            data4 = []
            for i, producto in enumerate(nombres_productos):
                x_labels = [f'{ano}' for ano in productos[producto].keys()]
                data4.append(go.Scatter(x=x_labels, y=tasa_rendimiento_productos[producto], name=producto, mode='lines+markers', hovertemplate='Tasa de Rendimiento: %{y:.2f}%'))

            layout4 = go.Layout(
                title='Comparación de Rendimientos de Inversión',
                xaxis=dict(title='Año'),
                yaxis=dict(title='Tasa de Rendimiento (%)'),
                hovermode='closest'
            )

            fig4 = go.Figure(data=data4, layout=layout4)
            plot_div4 = plot(fig4, output_type='div')

            return render(request, 'graficas.html', {'form': form, 'plot_div': plot_div, 'plot_div2': plot_div2, 'plot_div3': plot_div3, 'plot_div4': plot_div4})
    else:
        form = CSVUploadForm()
        return render(request, 'graficas.html', {'form': form})
