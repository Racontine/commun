# How to Enable Auto-Start

Follow these steps on your Raspberry Pi terminal:

1.  **Check User and Path**
    - Ensure the paths in `alice.service` are correct.
    - If you are user `pi`, edit the file to set `User=pi` and `WorkingDirectory=/home/pi/alice` etc.

2.  **Copy Service File**
    ```bash
    sudo cp alice.service /etc/systemd/system/alice.service
    ```

3.  **Reload Systemd**
    ```bash
    sudo systemctl daemon-reload
    ```

4.  **Enable and Start**
    ```bash
    sudo systemctl enable alice.service
    sudo systemctl start alice.service
    ```

5.  **Check Status**
    ```bash
    sudo systemctl status alice.service
    ```
    - You should see "Active: active (running)".

6.  **View Logs** (if needed)
    ```bash
    journalctl -u alice.service -f
    ```
