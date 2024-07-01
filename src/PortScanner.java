import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class PortScanner extends JFrame {

    private JTextField hostField;
    private JTextArea resultArea;
    private JButton scanButton;

    public PortScanner() {
        setTitle("Simple Port Scanner");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        initUI();
    }

    private void initUI() {
        JPanel panel = new JPanel(new GridLayout(2, 2));

        JLabel hostLabel = new JLabel("Host:");
        hostField = new JTextField();

        scanButton = new JButton("Scan");
        scanButton.addActionListener(new ScanButtonListener());

        resultArea = new JTextArea();
        resultArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(resultArea);

        panel.add(hostLabel);
        panel.add(hostField);
        panel.add(new JLabel());  // Empty cell in the grid
        panel.add(scanButton);

        add(panel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);
    }

    private class ScanButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            resultArea.setText("");  // Clear previous results
            String host = hostField.getText();

            int startPort = 1;
            int endPort = 65535;

            ExecutorService executor = Executors.newFixedThreadPool(100);  // Thread pool size

            for (int port = startPort; port <= endPort; port++) {
                int finalPort = port;
                executor.submit(() -> scanPort(host, finalPort));
            }

            executor.shutdown();
        }

        private void scanPort(String host, int port) {
            try (Socket socket = new Socket(host, port)) {
                SwingUtilities.invokeLater(() -> resultArea.append("Port " + port + " is open\n"));
            } catch (IOException e) {
                SwingUtilities.invokeLater(() -> resultArea.append("Port " + port + " is closed\n"));
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            PortScanner scannerGUI = new PortScanner();
            scannerGUI.setVisible(true);
        });
    }
}
