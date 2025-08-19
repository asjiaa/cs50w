// Render sentiment data

export function load_chart(result) {
    const container = document.querySelector('#sentiment-chart');
    container.innerHTML = '';

    const canvas = document.createElement('canvas');
    canvas.id = 'sentiment-canvas';
    container.append(canvas);

    const articles = result.articles.sort(
        (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
    );

    const labels = articles.map(article => new Date(article.timestamp));
    const compound = articles.map(article => article.sentiment.compound);
    const pos = articles.map(article => article.sentiment.pos);
    const neg = articles.map(article => article.sentiment.neg);
    const neu = articles.map(article => article.sentiment.neu);

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'compound',
                data: compound,
                borderColor: 'cyan',
                backgroundColor: 'lightblue',
                tension: 0.25,
                borderWidth: 3,
                pointRadius: 5
            },
            {
                label: 'pos',
                data: pos,
                borderColor: 'blue',
                backgroundColor: 'lightcyan',
                tension: 0.25,
                borderWidth: 2,
                pointRadius: 4
            },
            {
                label: 'neg',
                data: neg,
                borderColor: 'red',
                backgroundColor: 'mistyrose',
                tension: 0.25,
                borderWidth: 2,
                pointRadius: 4
            },
            {
                label: 'neu',
                data: neu,
                borderColor: 'goldenrod',
                backgroundColor: 'lightyellow',
                tension: 0.25,
                borderWidth: 2,
                pointRadius: 4
            }
        ]
    };

    const topic = result.topic;

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: `${topic.topic} (${topic.start} - ${topic.end})`,
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    title: function(context) {
                        const index = context[0].dataIndex;
                        const article = articles[index];
                        const date = new Date(article.timestamp).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric'
                        });
                        return `${article.headline} (${date})`;
                    },
                    label: function(context) {
                        const index = context.dataIndex;
                        const article = articles[index];
                        const label = context.dataset.label;
                        if (label === 'compound') return `compound: ${article.sentiment.compound}`;
                        if (label === 'pos') return `pos: ${article.sentiment.pos}`;
                        if (label === 'neg') return `neg: ${article.sentiment.neg}`;
                        if (label === 'neu') return `neu: ${article.sentiment.neu}`;
                        return `${label}: ${context.formattedValue}`;
                    },
                    afterBody: function(context) {
                        const index = context[0].dataIndex;
                        const article = articles[index];
                        return `${article.snippet}`;
                    }
                }
            },
            legend: {
                display: true,
                labels: {
                    generateLabels: function(chart) {
                        const origin = Chart.registry.getPlugin('legend').defaults.labels.generateLabels(chart);
                        return origin.map(item => {
                            let desc = '';
                            switch(item.text) {
                                case 'compound':
                                desc = 'an overall sentiment score based on pos, neg, neu scores';
                                break;
                            case 'pos':
                                desc = 'proportion of positive words in article headline and snippet';
                                break;
                            case 'neg':
                                desc = 'proportion of negative words in article headline and snippet';
                                break;
                            case 'neu':
                                desc = 'proportion of neutral words in article headline and snippet';
                                break;
                            }
                            return {
                                ...item,
                                description: desc
                            };
                        });
                    }
                },
                onHover: function(event, item, legend) {
                    if (item && item.description) {
                        legend.chart.canvas.title = item.description;
                    }
                },
                onLeave: function(event, item, legend) {
                    legend.chart.canvas.title = '';
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Date'
                },
                ticks: {
                    callback: function(value) {
                        const date = this.getLabelForValue(value);
                        const d = new Date(date);
                        return d.toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric'
                        });
                    },
                    maxRotation: 0,
                    autoSkip: true,
                    maxTicksLimit: 8
                },
                grid: { color: 'lightgray' }
            },
            y: {
                min: -1.2,
                max: 1.2,
                title: {
                    display: true,
                    text: 'Sentiment'
                },
                grid: { color: 'lightgray' }
            }
        },
        onClick: (evt, active) => {
            if (active.length > 0) {
                const point = active[0];
                const index = point.index;
                const article = articles[index];
                window.open(article.url, '_blank');
            }
        },
        hover: {
            mode: 'index',
            intersect: false,
            onHover: function(evt, active) {
                const chart = this;
                chart.data.datasets.forEach(dataset => {
                    dataset.pointRadius = dataset.data.map((_, idx) =>
                        active.length && idx === active[0].index ? 7 : 4
                    );
                });
                chart.update('none');
            }
        }
    };

    new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: data,
        options: options
    });
}