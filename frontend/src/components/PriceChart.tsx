/**
 * Simple SVG-based price line chart component.
 * No external dependencies required.
 */

import styles from "./PriceChart.module.css";

interface PriceData {
    date: string;
    close: number;
    high?: number | null;
    low?: number | null;
}

interface PriceChartProps {
    data: PriceData[];
    height?: number;
    showVolume?: boolean;
}

function PriceChart({ data, height = 200 }: PriceChartProps) {
    if (data.length === 0) {
        return (
            <div className={styles.empty}>
                No price data available
            </div>
        );
    }

    const sortedData = [...data].sort(
        (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    const prices = sortedData.map((d) => d.close);
    const minPrice = Math.min(...prices);
    const maxPrice = Math.max(...prices);
    const priceRange = maxPrice - minPrice || 1;

    const padding = { top: 20, right: 20, bottom: 30, left: 60 };
    const width = 100;
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;

    const scaleX = (index: number) =>
        padding.left + (index / (sortedData.length - 1 || 1)) * chartWidth;

    const scaleY = (price: number) =>
        padding.top + chartHeight - ((price - minPrice) / priceRange) * chartHeight;

    const pathData = sortedData
        .map((d, i) => {
            const x = scaleX(i);
            const y = scaleY(d.close);
            return `${i === 0 ? "M" : "L"} ${x} ${y}`;
        })
        .join(" ");

    const areaPath = `${pathData} L ${scaleX(sortedData.length - 1)} ${
        height - padding.bottom
    } L ${padding.left} ${height - padding.bottom} Z`;

    const firstPrice = sortedData[0]?.close || 0;
    const lastPrice = sortedData[sortedData.length - 1]?.close || 0;
    const priceChange = lastPrice - firstPrice;
    const priceChangePercent = firstPrice > 0 ? (priceChange / firstPrice) * 100 : 0;
    const isPositive = priceChange >= 0;

    const formatPrice = (price: number) => {
        if (price >= 1000) return `$${(price / 1000).toFixed(1)}k`;
        if (price >= 1) return `$${price.toFixed(2)}`;
        return `$${price.toFixed(4)}`;
    };

    const gridLines = 4;

    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <span className={styles.currentPrice}>
                    {formatPrice(lastPrice)}
                </span>
                <span
                    className={`${styles.change} ${
                        isPositive ? styles.positive : styles.negative
                    }`}>
                    {isPositive ? "+" : ""}
                    {priceChange.toFixed(2)} ({priceChangePercent.toFixed(2)}%)
                </span>
            </div>
            <svg
                className={styles.chart}
                viewBox={`0 0 ${width} ${height}`}
                preserveAspectRatio="none">
                {Array.from({ length: gridLines + 1 }).map((_, i) => {
                    const y = padding.top + (i / gridLines) * chartHeight;
                    const price = maxPrice - (i / gridLines) * priceRange;
                    return (
                        <g key={i}>
                            <line
                                x1={padding.left}
                                y1={y}
                                x2={width - padding.right}
                                y2={y}
                                className={styles.gridLine}
                            />
                            <text
                                x={padding.left - 5}
                                y={y + 3}
                                className={styles.axisLabel}
                                textAnchor="end">
                                {formatPrice(price)}
                            </text>
                        </g>
                    );
                })}

                <defs>
                    <linearGradient
                        id={`gradient-${isPositive ? "up" : "down"}`}
                        x1="0"
                        y1="0"
                        x2="0"
                        y2="1">
                        <stop
                            offset="0%"
                            stopColor={
                                isPositive
                                    ? "var(--color-accent-green)"
                                    : "var(--color-accent-red)"
                            }
                            stopOpacity="0.3"
                        />
                        <stop
                            offset="100%"
                            stopColor={
                                isPositive
                                    ? "var(--color-accent-green)"
                                    : "var(--color-accent-red)"
                            }
                            stopOpacity="0"
                        />
                    </linearGradient>
                </defs>

                <path
                    d={areaPath}
                    fill={`url(#gradient-${isPositive ? "up" : "down"})`}
                    className={styles.area}
                />

                <path
                    d={pathData}
                    fill="none"
                    className={`${styles.line} ${
                        isPositive ? styles.linePositive : styles.lineNegative
                    }`}
                />
            </svg>
            <div className={styles.footer}>
                <span className={styles.dateLabel}>
                    {sortedData[0]?.date}
                </span>
                <span className={styles.dateLabel}>
                    {sortedData[sortedData.length - 1]?.date}
                </span>
            </div>
        </div>
    );
}

export default PriceChart;
