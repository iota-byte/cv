import java.util.HashMap;
import java.util.Map;
import java.util.Iterator;
import java.util.concurrent.*;
import java.util.List;
import java.util.ArrayList;

public class CiscoSwitch {

    static class MacAddressEntry {
        String macAddress;
        String port;
        long lastSeen;

        MacAddressEntry(String macAddress, String port) {
            this.macAddress = macAddress;
            this.port = port;
            this.lastSeen = System.currentTimeMillis();
        }

        void updateLastSeen() {
            this.lastSeen = System.currentTimeMillis();
        }
    }

    private Map<String, MacAddressEntry> camTable;
    private long agingTime;
    private int maxMacAddressesPerPort;
    private ExecutorService executorService;

    // Constructor to initialize the switch
    public CiscoSwitch(int maxMacAddressesPerPort, long agingTime) {
        this.camTable = new HashMap<>();
        this.maxMacAddressesPerPort = maxMacAddressesPerPort;
        this.agingTime = agingTime;
        this.executorService = Executors.newCachedThreadPool();
    }

    // Learn a MAC address on a port
    public void learnMacAddress(String macAddress, String port) {
        MacAddressEntry entry = camTable.get(macAddress);
        if (entry != null) {
            entry.updateLastSeen();
        } else {
            if (getMacAddressesCountForPort(port) < maxMacAddressesPerPort) {
                camTable.put(macAddress, new MacAddressEntry(macAddress, port));
            } else {
                System.out.println("Port " + port + " has exceeded max MAC addresses limit.");
            }
        }
    }

    // Forward frames in parallel based on MAC addresses
    public void forwardFramesParallel(String[] macAddresses) {
        List<Future<String>> futures = new ArrayList<>();
        for (String macAddress : macAddresses) {
            futures.add(executorService.submit(() -> forwardFrame(macAddress)));
        }
        for (Future<String> future : futures) {
            try {
                System.out.println(future.get());
            } catch (InterruptedException | ExecutionException e) {
                System.err.println("Error during forwarding: " + e.getMessage());
            }
        }
    }

    // Forward a single frame based on MAC address
    public String forwardFrame(String macAddress) {
        MacAddressEntry entry = camTable.get(macAddress);
        if (entry != null) {
            return "Forwarding frame to port " + entry.port;
        } else {
            return "Flooding frame to all ports (unknown MAC address)";
        }
    }

    // Age out old MAC addresses from the table
    public void ageOutMacAddresses() {
        long currentTime = System.currentTimeMillis();
        Iterator<Map.Entry<String, MacAddressEntry>> iterator = camTable.entrySet().iterator();
        while (iterator.hasNext()) {
            Map.Entry<String, MacAddressEntry> entry = iterator.next();
            if (currentTime - entry.getValue().lastSeen > agingTime) {
                System.out.println("Aging out MAC address: " + entry.getKey());
                iterator.remove();
            }
        }
    }

    // Helper method to count MAC addresses on a specific port
    private int getMacAddressesCountForPort(String port) {
        int count = 0;
        for (MacAddressEntry entry : camTable.values()) {
            if (entry.port.equals(port)) {
                count++;
            }
        }
        return count;
    }

    // Print the CAM table for debugging or monitoring
    public void printCamTable() {
        System.out.println("CAM Table:");
        for (MacAddressEntry entry : camTable.values()) {
            System.out.println("MAC Address: " + entry.macAddress + ", Port: " + entry.port + ", Last Seen: " + entry.lastSeen);
        }
    }

    public static void main(String[] args) {
        CiscoSwitch switch1 = new CiscoSwitch(2, 10000);

        switch1.learnMacAddress("00:11:22:33:44:55", "Gig1/0/1");
        switch1.learnMacAddress("66:77:88:99:00:11", "Gig1/0/2");
        switch1.learnMacAddress("00:11:22:33:44:66", "Gig1/0/1");

        String[] macAddressesToForward = {"00:11:22:33:44:55", "AA:BB:CC:DD:EE:FF", "66:77:88:99:00:11"};
        switch1.forwardFramesParallel(macAddressesToForward);

        switch1.printCamTable();

        try {
            Thread.sleep(15000); // Wait for aging
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        switch1.ageOutMacAddresses();

        switch1.printCamTable();
    }
}
