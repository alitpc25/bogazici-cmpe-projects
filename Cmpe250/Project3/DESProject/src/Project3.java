import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.PriorityQueue;
import java.io.BufferedReader;
import java.io.FileReader;

public class Project3 {
	
	public static void main(String[] args) {
		try {
			File readObject = new File(args[0]); // args[0] = input dir
		    BufferedReader myReader = new BufferedReader(new FileReader(readObject));
		    FileWriter myWriter = new FileWriter(args[1]);
		    String[] lines = myReader.readLine().split(" ");
		    int numOfALines = Integer.valueOf(lines[0]);
		    int numOfFLines = Integer.valueOf(lines[1]);
		    
		    HashMap<String, ACC> mapOfACC = new HashMap<>();
		    int temp = numOfALines;
			while(temp > 0) {
				String[] data = myReader.readLine().split(" ");
				String accCode = data[0];
				ACC acc = new ACC(accCode);
				mapOfACC.put(accCode, acc);
				LinearProbingHashTable airports = acc.getHashTable();
				for(int i=1; i<data.length; i++) {
					ATC atc = new ATC(accCode, data[i]);
					int ind = airports.insert(data[i], atc);
					atc.setAtcCode(accCode+String.format("%03d" ,ind));
				}
				temp--;
			}
			
			PriorityQueue<Flight> eventQueue = new PriorityQueue<>(numOfFLines, new EventComparator());
			temp = numOfFLines;
		    while (temp > 0) {
		        String[] data = myReader.readLine().split(" ");
		        int admissionTime = Integer.valueOf(data[0]);
		        String flightCode = data[1];
		        String accCode = data[2];
		        String departureAirportCode = data[3];
		        String arrivalAirportCode = data[4];
		        ACC acc = mapOfACC.get(accCode);
		        ATC departureAtc = acc.getHashTable().get(departureAirportCode);
		        ATC arrivalAtc = acc.getHashTable().get(arrivalAirportCode);
		        Flight flight = new Flight(flightCode, 1, departureAtc, arrivalAtc, acc, admissionTime);
		        List<Integer> ops = flight.getOperations();
		        for(int i=5; i<data.length; i++) {
		        	ops.add(Integer.valueOf(data[i]));
		        }
		        eventQueue.add(flight);
		        temp--;
		    }
		    
		    // Operations
		    long[] clocks = new long[numOfALines];
		    int index = 0;
		    
		    while(!eventQueue.isEmpty()) {
		    	Flight fly = eventQueue.poll();
		    	ACC acc = fly.getAcc();
		    	clocks[index] = fly.getAdmissionTime();
		    	PriorityQueue<Flight> flights = new PriorityQueue<>(numOfFLines, new EventComparator());
		    	List<ATC> atcs = new ArrayList<>();
		    	flights.add(fly);
		    	while(!eventQueue.isEmpty() && eventQueue.peek().getAcc().getAccCode().equals(acc.getAccCode())) {
		    		Flight f = eventQueue.poll();
		    		flights.add(f);
		    		if(!atcs.contains(f.getDepartureAirport())) {
		    			atcs.add(f.getDepartureAirport());
		    		}
		    		if(!atcs.contains(f.getLandingAirport())) {
		    			atcs.add(f.getLandingAirport());
		    		}
		    	}
		    	Simulation s = new Simulation(acc, new ArrayList<>(atcs), new PriorityQueue<>(flights), flights.peek().getAdmissionTime(), flights.size());
		    	String res = s.start();
		    	myWriter.write(res);
		    	mapOfACC.remove(acc.getAccCode());
		    	index++;
	    	}
		    for (String key : mapOfACC.keySet()) {
		    	String airport = "";
		    	for (int keyOfTable : mapOfACC.get(key).getHashTable().getKeySet()) {
		    		airport += " " + mapOfACC.get(key).getHashTable().getByIndex(keyOfTable).getAirportCode() + String.format("%03d" ,keyOfTable);
		    	}
		    	myWriter.write(mapOfACC.get(key).getAccCode() + " " + 0 + airport +"\n");
		    }
		    
		    myReader.close();
		    myWriter.close();
		} catch (IOException e) {
		    e.printStackTrace();
		}
	}
}

class EventComparator implements Comparator<Flight>{
	@Override
	public int compare(Flight o1, Flight o2) {
		if(!o1.getAcc().getAccCode().equals(o2.getAcc().getAccCode())) {
			return o1.getAcc().getAccCode().compareTo(o2.getAcc().getAccCode());
		} 
		if(o1.getAdmissionTime() != o2.getAdmissionTime()) {
			return (int) (o1.getAdmissionTime() - o2.getAdmissionTime());
		}
		return o1.getFlightCode().compareTo(o2.getFlightCode());
	}
}
