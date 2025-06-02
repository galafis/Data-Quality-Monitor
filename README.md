# Data Quality Monitor

[English](#english) | [Português](#português)

## English

### Overview
Comprehensive data quality monitoring system built with Python and Flask. Features automated data validation, quality metrics calculation, anomaly detection, and real-time monitoring dashboards for ensuring data integrity across your data pipeline.

### Features
- **Automated Validation**: Rule-based data quality checks
- **Quality Metrics**: Completeness, accuracy, consistency, validity
- **Anomaly Detection**: Statistical outlier identification
- **Real-Time Monitoring**: Live data quality dashboards
- **Alert System**: Configurable quality threshold alerts
- **Historical Tracking**: Quality trends and improvement tracking
- **Multiple Data Sources**: CSV, database, API data validation
- **Custom Rules**: Flexible validation rule configuration

### Technologies Used
- **Python 3.8+**
- **Flask**: Web framework and dashboard
- **Pandas**: Data manipulation and analysis
- **NumPy**: Statistical calculations
- **Matplotlib**: Data visualization
- **SQLite**: Quality metrics storage

### Installation

1. Clone the repository:
```bash
git clone https://github.com/galafis/Data-Quality-Monitor.git
cd Data-Quality-Monitor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the quality monitor:
```bash
python quality_monitor.py
```

4. Open your browser to `http://localhost:5000`

### Usage

#### Web Interface
1. **Upload Data**: Submit datasets for quality analysis
2. **Configure Rules**: Set up validation rules and thresholds
3. **Monitor Dashboard**: View real-time quality metrics
4. **Quality Reports**: Generate detailed quality assessments
5. **Alert Management**: Configure and manage quality alerts

#### API Endpoints

**Analyze Data Quality**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "file=@data.csv" \
  -F "dataset_name=customer_data"
```

**Get Quality Metrics**
```bash
curl -X GET http://localhost:5000/api/metrics/customer_data
```

**Configure Validation Rules**
```bash
curl -X POST http://localhost:5000/api/rules \
  -H "Content-Type: application/json" \
  -d '{"dataset": "customer_data", "rules": [{"column": "email", "type": "email_format"}]}'
```

#### Python API
```python
from quality_monitor import DataQualityMonitor

# Initialize monitor
monitor = DataQualityMonitor()

# Analyze data quality
results = monitor.analyze_dataset('customer_data.csv')

# Get quality metrics
metrics = monitor.get_quality_metrics(results)
print(f"Completeness: {metrics['completeness']:.2%}")
print(f"Validity: {metrics['validity']:.2%}")

# Set up monitoring
monitor.add_validation_rule('email', 'email_format')
monitor.start_monitoring('customer_data')
```

### Quality Dimensions

#### Completeness
- **Missing Values**: Identify null and empty values
- **Required Fields**: Validate mandatory column presence
- **Record Completeness**: Assess overall record integrity
- **Completeness Score**: Percentage of complete data

#### Accuracy
- **Format Validation**: Email, phone, date format checks
- **Range Validation**: Numeric range and boundary checks
- **Pattern Matching**: Regular expression validation
- **Reference Data**: Lookup table validation

#### Consistency
- **Cross-Field Validation**: Logical relationship checks
- **Duplicate Detection**: Identify duplicate records
- **Data Type Consistency**: Ensure consistent data types
- **Business Rule Validation**: Custom business logic checks

#### Validity
- **Schema Compliance**: Data structure validation
- **Constraint Validation**: Primary key and foreign key checks
- **Domain Validation**: Acceptable value range checks
- **Referential Integrity**: Cross-table relationship validation

### Validation Rules

#### Built-in Rules
- **Email Format**: Valid email address validation
- **Phone Format**: Phone number format validation
- **Date Format**: Date and datetime validation
- **Numeric Range**: Min/max value validation
- **String Length**: Text length validation
- **Required Field**: Non-null value validation

#### Custom Rules
```python
# Define custom validation rule
def custom_age_validation(value):
    return 0 <= value <= 150

# Register custom rule
monitor.add_custom_rule('age', custom_age_validation)
```

### Anomaly Detection

#### Statistical Methods
- **Z-Score**: Standard deviation-based outlier detection
- **IQR Method**: Interquartile range outlier identification
- **Isolation Forest**: Machine learning-based anomaly detection
- **Moving Average**: Time series anomaly detection

#### Threshold Configuration
- **Static Thresholds**: Fixed quality score limits
- **Dynamic Thresholds**: Adaptive threshold adjustment
- **Percentile-Based**: Quality score percentile thresholds
- **Historical Baselines**: Compare against historical quality

### Monitoring Dashboard

#### Real-Time Metrics
- **Quality Score**: Overall data quality percentage
- **Trend Analysis**: Quality improvement/degradation trends
- **Issue Distribution**: Breakdown of quality issues by type
- **Alert Status**: Current alert status and notifications

#### Visualizations
- **Quality Trends**: Time series quality score charts
- **Issue Heatmaps**: Quality issues by column and severity
- **Completeness Charts**: Missing data visualization
- **Distribution Plots**: Data distribution and outlier visualization

### Alert System

#### Alert Types
- **Quality Threshold**: Quality score below threshold
- **Anomaly Detection**: Statistical anomaly alerts
- **Rule Violation**: Validation rule failure alerts
- **Data Drift**: Significant data distribution changes

#### Notification Channels
- **Email Alerts**: Quality issue email notifications
- **Dashboard Alerts**: Real-time dashboard notifications
- **API Webhooks**: Programmatic alert integration
- **Log Alerts**: Quality issue logging

### Quality Reports

#### Summary Reports
- **Executive Summary**: High-level quality overview
- **Detailed Analysis**: Column-by-column quality assessment
- **Trend Reports**: Quality improvement tracking
- **Issue Reports**: Detailed quality issue breakdown

#### Export Formats
- **PDF Reports**: Professional quality reports
- **CSV Exports**: Quality metrics data export
- **JSON API**: Programmatic report access
- **Dashboard Screenshots**: Visual report exports

### Configuration
Configure quality monitoring in `config.json`:
```json
{
  "quality_thresholds": {
    "completeness": 0.95,
    "accuracy": 0.90,
    "consistency": 0.85,
    "validity": 0.95
  },
  "anomaly_detection": {
    "method": "z_score",
    "threshold": 3.0,
    "window_size": 100
  },
  "alerts": {
    "email_enabled": true,
    "threshold_alerts": true,
    "anomaly_alerts": true
  }
}
```

### Integration
- **Data Pipelines**: Integrate with ETL/ELT processes
- **CI/CD**: Quality gates in deployment pipelines
- **Data Catalogs**: Quality metadata integration
- **Monitoring Tools**: Integration with existing monitoring systems

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Português

### Visão Geral
Sistema abrangente de monitoramento de qualidade de dados construído com Python e Flask. Apresenta validação automatizada de dados, cálculo de métricas de qualidade, detecção de anomalias e dashboards de monitoramento em tempo real para garantir a integridade dos dados em seu pipeline de dados.

### Funcionalidades
- **Validação Automatizada**: Verificações de qualidade baseadas em regras
- **Métricas de Qualidade**: Completude, precisão, consistência, validade
- **Detecção de Anomalias**: Identificação estatística de outliers
- **Monitoramento em Tempo Real**: Dashboards de qualidade de dados ao vivo
- **Sistema de Alertas**: Alertas configuráveis de limites de qualidade
- **Rastreamento Histórico**: Tendências de qualidade e rastreamento de melhorias
- **Múltiplas Fontes de Dados**: Validação de dados CSV, banco de dados, API
- **Regras Personalizadas**: Configuração flexível de regras de validação

### Tecnologias Utilizadas
- **Python 3.8+**
- **Flask**: Framework web e dashboard
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Cálculos estatísticos
- **Matplotlib**: Visualização de dados
- **SQLite**: Armazenamento de métricas de qualidade

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/galafis/Data-Quality-Monitor.git
cd Data-Quality-Monitor
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o monitor de qualidade:
```bash
python quality_monitor.py
```

4. Abra seu navegador em `http://localhost:5000`

### Uso

#### Interface Web
1. **Upload de Dados**: Submeter datasets para análise de qualidade
2. **Configurar Regras**: Configurar regras de validação e limites
3. **Dashboard de Monitoramento**: Visualizar métricas de qualidade em tempo real
4. **Relatórios de Qualidade**: Gerar avaliações detalhadas de qualidade
5. **Gerenciamento de Alertas**: Configurar e gerenciar alertas de qualidade

#### Endpoints da API

**Analisar Qualidade dos Dados**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "file=@dados.csv" \
  -F "dataset_name=dados_cliente"
```

**Obter Métricas de Qualidade**
```bash
curl -X GET http://localhost:5000/api/metrics/dados_cliente
```

**Configurar Regras de Validação**
```bash
curl -X POST http://localhost:5000/api/rules \
  -H "Content-Type: application/json" \
  -d '{"dataset": "dados_cliente", "rules": [{"column": "email", "type": "email_format"}]}'
```

#### API Python
```python
from quality_monitor import DataQualityMonitor

# Inicializar monitor
monitor = DataQualityMonitor()

# Analisar qualidade dos dados
results = monitor.analyze_dataset('dados_cliente.csv')

# Obter métricas de qualidade
metrics = monitor.get_quality_metrics(results)
print(f"Completude: {metrics['completeness']:.2%}")
print(f"Validade: {metrics['validity']:.2%}")

# Configurar monitoramento
monitor.add_validation_rule('email', 'email_format')
monitor.start_monitoring('dados_cliente')
```

### Dimensões de Qualidade

#### Completude
- **Valores Ausentes**: Identificar valores nulos e vazios
- **Campos Obrigatórios**: Validar presença de colunas obrigatórias
- **Completude de Registro**: Avaliar integridade geral do registro
- **Score de Completude**: Porcentagem de dados completos

#### Precisão
- **Validação de Formato**: Verificações de formato de email, telefone, data
- **Validação de Intervalo**: Verificações de intervalo numérico e limites
- **Correspondência de Padrões**: Validação por expressão regular
- **Dados de Referência**: Validação de tabela de lookup

#### Consistência
- **Validação Cross-Field**: Verificações de relacionamento lógico
- **Detecção de Duplicatas**: Identificar registros duplicados
- **Consistência de Tipo de Dados**: Garantir tipos de dados consistentes
- **Validação de Regras de Negócio**: Verificações de lógica de negócio personalizada

#### Validade
- **Conformidade de Schema**: Validação de estrutura de dados
- **Validação de Restrições**: Verificações de chave primária e estrangeira
- **Validação de Domínio**: Verificações de intervalo de valores aceitáveis
- **Integridade Referencial**: Validação de relacionamento cross-table

### Regras de Validação

#### Regras Built-in
- **Formato de Email**: Validação de endereço de email válido
- **Formato de Telefone**: Validação de formato de número de telefone
- **Formato de Data**: Validação de data e datetime
- **Intervalo Numérico**: Validação de valor min/max
- **Comprimento de String**: Validação de comprimento de texto
- **Campo Obrigatório**: Validação de valor não-nulo

#### Regras Personalizadas
```python
# Definir regra de validação personalizada
def custom_age_validation(value):
    return 0 <= value <= 150

# Registrar regra personalizada
monitor.add_custom_rule('age', custom_age_validation)
```

### Detecção de Anomalias

#### Métodos Estatísticos
- **Z-Score**: Detecção de outlier baseada em desvio padrão
- **Método IQR**: Identificação de outlier por intervalo interquartil
- **Isolation Forest**: Detecção de anomalia baseada em machine learning
- **Média Móvel**: Detecção de anomalia em séries temporais

#### Configuração de Limites
- **Limites Estáticos**: Limites fixos de score de qualidade
- **Limites Dinâmicos**: Ajuste adaptativo de limites
- **Baseado em Percentil**: Limites de percentil de score de qualidade
- **Baselines Históricos**: Comparar com qualidade histórica

### Dashboard de Monitoramento

#### Métricas em Tempo Real
- **Score de Qualidade**: Porcentagem geral de qualidade dos dados
- **Análise de Tendência**: Tendências de melhoria/degradação da qualidade
- **Distribuição de Problemas**: Breakdown de problemas de qualidade por tipo
- **Status de Alertas**: Status atual de alertas e notificações

#### Visualizações
- **Tendências de Qualidade**: Gráficos de séries temporais de score de qualidade
- **Heatmaps de Problemas**: Problemas de qualidade por coluna e severidade
- **Gráficos de Completude**: Visualização de dados ausentes
- **Gráficos de Distribuição**: Distribuição de dados e visualização de outliers

### Sistema de Alertas

#### Tipos de Alertas
- **Limite de Qualidade**: Score de qualidade abaixo do limite
- **Detecção de Anomalia**: Alertas de anomalia estatística
- **Violação de Regra**: Alertas de falha de regra de validação
- **Data Drift**: Mudanças significativas na distribuição de dados

#### Canais de Notificação
- **Alertas por Email**: Notificações por email de problemas de qualidade
- **Alertas de Dashboard**: Notificações em tempo real no dashboard
- **Webhooks de API**: Integração programática de alertas
- **Alertas de Log**: Logging de problemas de qualidade

### Relatórios de Qualidade

#### Relatórios de Resumo
- **Resumo Executivo**: Visão geral de qualidade de alto nível
- **Análise Detalhada**: Avaliação de qualidade coluna por coluna
- **Relatórios de Tendência**: Rastreamento de melhoria de qualidade
- **Relatórios de Problemas**: Breakdown detalhado de problemas de qualidade

#### Formatos de Exportação
- **Relatórios PDF**: Relatórios de qualidade profissionais
- **Exportações CSV**: Exportação de dados de métricas de qualidade
- **API JSON**: Acesso programático a relatórios
- **Screenshots de Dashboard**: Exportações de relatórios visuais

### Configuração
Configure o monitoramento de qualidade em `config.json`:
```json
{
  "quality_thresholds": {
    "completeness": 0.95,
    "accuracy": 0.90,
    "consistency": 0.85,
    "validity": 0.95
  },
  "anomaly_detection": {
    "method": "z_score",
    "threshold": 3.0,
    "window_size": 100
  },
  "alerts": {
    "email_enabled": true,
    "threshold_alerts": true,
    "anomaly_alerts": true
  }
}
```

### Integração
- **Pipelines de Dados**: Integrar com processos ETL/ELT
- **CI/CD**: Gates de qualidade em pipelines de deployment
- **Catálogos de Dados**: Integração de metadados de qualidade
- **Ferramentas de Monitoramento**: Integração com sistemas de monitoramento existentes

### Contribuindo
1. Faça um fork do repositório
2. Crie uma branch de feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adicionar nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

### Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

