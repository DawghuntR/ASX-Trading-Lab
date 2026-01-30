#!/bin/bash
# ASX Trading Lab - Systemd Installation Script
# Run as: sudo ./install.sh
#
# This script installs the systemd service and timer for the ASX jobs runner.

set -euo pipefail

# Configuration
SERVICE_NAME="asx-jobs"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEMD_DIR="/etc/systemd/system"

echo "Installing ASX Trading Lab systemd units..."

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    echo "Error: This script must be run as root (sudo)" >&2
    exit 1
fi

# Check timezone
CURRENT_TZ=$(timedatectl show --property=Timezone --value 2>/dev/null || echo "unknown")
if [[ "$CURRENT_TZ" != "Australia/Sydney" ]]; then
    echo "Warning: System timezone is '$CURRENT_TZ', not 'Australia/Sydney'"
    echo "The timer is configured for 12:00 local time."
    echo "To set timezone: sudo timedatectl set-timezone Australia/Sydney"
    echo ""
fi

# Copy service files
echo "Copying service files to $SYSTEMD_DIR..."
cp "$SCRIPT_DIR/systemd/$SERVICE_NAME.service" "$SYSTEMD_DIR/"
cp "$SCRIPT_DIR/systemd/$SERVICE_NAME.timer" "$SYSTEMD_DIR/"

# Set permissions
chmod 644 "$SYSTEMD_DIR/$SERVICE_NAME.service"
chmod 644 "$SYSTEMD_DIR/$SERVICE_NAME.timer"

# Reload systemd
echo "Reloading systemd daemon..."
systemctl daemon-reload

# Enable timer (but don't start yet)
echo "Enabling timer..."
systemctl enable "$SERVICE_NAME.timer"

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Ensure the jobs runner is installed:"
echo "     cd /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs"
echo "     pip install -e ."
echo ""
echo "  2. Create the environment file:"
echo "     cp .env.example .env"
echo "     # Edit .env with your Supabase credentials"
echo ""
echo "  3. Test the service manually:"
echo "     sudo systemctl start $SERVICE_NAME.service"
echo "     sudo journalctl -u $SERVICE_NAME.service -f"
echo ""
echo "  4. Start the timer:"
echo "     sudo systemctl start $SERVICE_NAME.timer"
echo ""
echo "  5. Check timer status:"
echo "     systemctl list-timers | grep $SERVICE_NAME"
echo ""
