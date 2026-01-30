import styles from "./StatusBadge.module.css";

interface StatusBadgeProps {
    status: "healthy" | "warning" | "error" | "unknown";
    label: string;
}

function StatusBadge({ status, label }: StatusBadgeProps) {
    return (
        <span className={`${styles.badge} ${styles[status]}`}>{label}</span>
    );
}

export default StatusBadge;
