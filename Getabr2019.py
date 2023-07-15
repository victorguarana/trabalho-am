import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def converter_para_minutos(duracao):
    try:
        hours, minutes = duracao.split(':')
        return int(hours) * 60 + int(minutes)
    except:
        return 0


def analisePadraoUso(data):

    # Converter as colunas de data e hora para o formato adequado
    data['DataIni'] = pd.to_datetime(data['DataIni'], format='%m/%d/%y %H:%M:%S')
    data['HoraIni'] = pd.to_datetime(data['HoraIni'], format='%m/%d/%y %H:%M:%S')

    # Criar uma coluna com a data e hora completa
    data['DataHoraIni'] = data['DataIni'] + pd.to_timedelta(data['HoraIni'].dt.hour, unit='h') + pd.to_timedelta(
        data['HoraIni'].dt.minute, unit='m') + pd.to_timedelta(data['HoraIni'].dt.second, unit='s')

    # Agrupar os dados por hora e calcular a média do total de giros em cada hora
    dados_por_hora = data.groupby('DataHoraIni')['TotalGiros'].mean()

    # Plotar o gráfico de linha
    plt.figure(figsize=(12, 6))
    plt.plot(dados_por_hora.index, dados_por_hora.values)
    plt.xlabel('Data e Hora')
    plt.ylabel('Total de Giros (Média)')
    plt.title('Análise do padrão de uso - Total de Giros ao longo do tempo')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()


def analiseDuraçaoMedia(data):


    # Converter as colunas de data e hora para o formato adequado
    data['DataIni'] = pd.to_datetime(data['DataIni'], format='%m/%d/%y %H:%M:%S')
    data['HoraIni'] = pd.to_datetime(data['HoraIni'], format='%m/%d/%y %H:%M:%S')
    data['DataFim'] = pd.to_datetime(data['DataFim'], format='%m/%d/%y %H:%M:%S')
    data['HoraFim'] = pd.to_datetime(data['HoraFim'], format='%m/%d/%y %H:%M:%S')

    # Criar uma coluna com a data e hora completa de início e fim da viagem
    data['DataHoraIni'] = data['DataIni'] + pd.to_timedelta(data['HoraIni'].dt.hour, unit='h') + pd.to_timedelta(
        data['HoraIni'].dt.minute, unit='m') + pd.to_timedelta(data['HoraIni'].dt.second, unit='s')
    data['DataHoraFim'] = data['DataFim'] + pd.to_timedelta(data['HoraFim'].dt.hour, unit='h') + pd.to_timedelta(
        data['HoraFim'].dt.minute, unit='m') + pd.to_timedelta(data['HoraFim'].dt.second, unit='s')

    # Calcular a duração da viagem em minutos
    data['DuracaoViagemMin'] = (data['DataHoraFim'] - data['DataHoraIni']).dt.total_seconds() / 60

    # Agrupar os dados por linha e hora e calcular a duração média das viagens
    duracao_media_por_linha_hora = data.groupby(['Linha', 'HoraIni'])['DuracaoViagemMin'].mean().reset_index()

    # Ordenar o dataframe por duração média de viagem
    duracao_media_por_linha_hora = duracao_media_por_linha_hora.sort_values(by='DuracaoViagemMin', ascending=False)

    # Plotar o gráfico de barras horizontais com as durações médias de viagem para cada linha
    plt.figure(figsize=(10, 8))
    plt.barh(
        duracao_media_por_linha_hora['Linha'] + ' - ' + duracao_media_por_linha_hora['HoraIni'].dt.strftime('%H:%M'),
        duracao_media_por_linha_hora['DuracaoViagemMin'], color='skyblue')
    plt.xlabel('Duração Média da Viagem (min)')
    plt.ylabel('Linha - Hora de partida')
    plt.title('Análise da duração média das viagens por linha e horário')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # Imprimir o resultado de duração média de viagem mais longa e mais curta
    print('Duração média de viagem mais longa:')
    print(duracao_media_por_linha_hora.iloc[0])
    print('\nDuração média de viagem mais curta:')
    print(duracao_media_por_linha_hora.iloc[-1])


def analiseQuilometragemMedia(data):
    # Converter as colunas de data e hora para o formato adequado
    data['DataIni'] = pd.to_datetime(data['DataIni'], format='%m/%d/%y %H:%M:%S')
    data['HoraIni'] = pd.to_datetime(data['HoraIni'], format='%m/%d/%y %H:%M:%S')
    data['DataFim'] = pd.to_datetime(data['DataFim'], format='%m/%d/%y %H:%M:%S')
    data['HoraFim'] = pd.to_datetime(data['HoraFim'], format='%m/%d/%y %H:%M:%S')

    # Criar uma coluna com a data e hora completa de início e fim da viagem
    data['DataHoraIni'] = data['DataIni'] + pd.to_timedelta(data['HoraIni'].dt.hour, unit='h') + pd.to_timedelta(
        data['HoraIni'].dt.minute, unit='m') + pd.to_timedelta(data['HoraIni'].dt.second, unit='s')
    data['DataHoraFim'] = data['DataFim'] + pd.to_timedelta(data['HoraFim'].dt.hour, unit='h') + pd.to_timedelta(
        data['HoraFim'].dt.minute, unit='m') + pd.to_timedelta(data['HoraFim'].dt.second, unit='s')

    # Calcular a quilometragem percorrida em cada viagem
    data['KmPercorridos'] = data['KmPerc']

    # Agrupar os dados por linha e hora e calcular a quilometragem média percorrida nas viagens
    quilometragem_media_por_linha_hora = data.groupby(['Linha', 'HoraIni'])['KmPercorridos'].mean().reset_index()

    # Ordenar o dataframe por quilometragem média percorrida
    quilometragem_media_por_linha_hora = quilometragem_media_por_linha_hora.sort_values(by='KmPercorridos',
                                                                                        ascending=False)

    # Plotar o gráfico de barras horizontais com a quilometragem média percorrida para cada linha e horário
    plt.figure(figsize=(10, 8))
    plt.barh(
        quilometragem_media_por_linha_hora['Linha'] + ' - ' + quilometragem_media_por_linha_hora['HoraIni'].dt.strftime(
            '%H:%M'), quilometragem_media_por_linha_hora['KmPercorridos'], color='lightgreen')
    plt.xlabel('Quilometragem Média Percorrida (km)')
    plt.ylabel('Linha - Hora de partida')
    plt.title('Análise da quilometragem média percorrida por linha e horário (amostra de metade do arquivo)')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')  # Ajustar a rotação dos labels do eixo x
    plt.tight_layout()
    plt.show()

    # Imprimir o resultado de quilometragem média percorrida maior e menor
    print('Quilometragem média percorrida maior:')
    print(quilometragem_media_por_linha_hora.iloc[0])
    print('\nQuilometragem média percorrida menor:')
    print(quilometragem_media_por_linha_hora.iloc[-1])

def analiseSentidoViagens(data):
    # Contando o número de viagens de ida e volta
    viagens_por_sentido = data['Sentido'].value_counts()

    # Criando o gráfico de barras
    plt.figure(figsize=(8, 6))
    sns.barplot(x=viagens_por_sentido.index, y=viagens_por_sentido.values, palette='viridis')

    # Adicionando título e rótulos
    plt.title('Número de Viagens por Sentido', fontsize=16)
    plt.xlabel('Sentido', fontsize=14)
    plt.ylabel('Número de Viagens', fontsize=14)

    # Exibindo o gráfico
    plt.show()


def analisePontualidadeViagens(data):
    # Converter as colunas de data e hora para o formato datetime
    data['DataFim'] = pd.to_datetime(data['DataFim'], format='%m/%d/%y %H:%M:%S', errors='coerce')
    data['HoraFim'] = pd.to_datetime(data['HoraFim'], format='%H:%M:%S', errors='coerce')
    data['DataIni'] = pd.to_datetime(data['DataIni'], format='%m/%d/%y %H:%M:%S', errors='coerce')
    data['HoraIni'] = pd.to_datetime(data['HoraIni'], format='%H:%M:%S', errors='coerce')

    # Filtrar apenas as linhas com datas e horas válidas
    data = data.dropna(subset=['DataFim', 'HoraFim', 'DataIni', 'HoraIni'])

    # Calcular a diferença entre o horário previsto e o horário real de chegada em minutos
    data['DiferencaChegada'] = (data['DataFim'] + pd.to_timedelta(data['HoraFim'].dt.hour, unit='h') + pd.to_timedelta(data['HoraFim'].dt.minute, unit='m') + pd.to_timedelta(data['HoraFim'].dt.second, unit='s') - data['DataIni'] - pd.to_timedelta(data['HoraIni'].dt.hour, unit='h') - pd.to_timedelta(data['HoraIni'].dt.minute, unit='m') - pd.to_timedelta(data['HoraIni'].dt.second, unit='s')).dt.total_seconds() / 60

    # Plotar gráfico de dispersão para visualizar a diferença entre o horário previsto e o horário real de chegada
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x='DiferencaChegada', y='TotalGiros')
    plt.xlabel('Diferença entre o horário previsto e o horário real de chegada (minutos)')
    plt.ylabel('Total de giros')
    plt.title('Análise de Pontualidade das Viagens')
    plt.show()

    # Plotar histograma para visualizar a distribuição da diferença entre o horário previsto e o horário real de chegada
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x='DiferencaChegada', bins=20, kde=True)
    plt.xlabel('Diferença entre o horário previsto e o horário real de chegada (minutos)')
    plt.ylabel('Frequência')
    plt.title('Distribuição da Pontualidade das Viagens')
    plt.show()

# Carregar o conjunto de dados
data = pd.read_csv('C:/Users/User/Documents/GitHub/trabalho-am/abr2019.csv', sep=',')

# Reduzir o conjunto de dados
data = data.sample(frac=0.5, random_state=42)


analisePadraoUso(data)
analiseDuraçaoMedia(data)
analiseQuilometragemMedia(data)
analiseSentidoViagens(data)
analisePontualidadeViagens(data)
