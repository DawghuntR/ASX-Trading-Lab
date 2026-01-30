import styles from "./Card.module.css";

interface CardProps {
    title?: string;
    children: React.ReactNode;
    className?: string;
}

function Card({ title, children, className = "" }: CardProps) {
    return (
        <div className={`${styles.card} ${className}`}>
            {title && <h3 className={styles.title}>{title}</h3>}
            <div className={styles.content}>{children}</div>
        </div>
    );
}

export default Card;
