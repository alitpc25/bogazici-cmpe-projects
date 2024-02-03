import java.util.PriorityQueue;
import java.util.Queue;

public class ATC {
	// Processes take off and land operations.
	
	private String airportCode;
	private String atcCode; // 7 char = 4 ch from ACC + 3 from [0,999], fill zeros to front.
	private Queue<Flight> readyQueue;
	
	public ATC(String atcCode, String airportCode) {
		this.atcCode = atcCode;
		this.airportCode = airportCode;
		this.readyQueue = new PriorityQueue<>(new FlightComparatorAtc());
	}

	public String getAtcCode() {
		return atcCode;
	}

	public void setAtcCode(String atcCode) {
		this.atcCode = atcCode;
	}
	
	public String getAirportCode() {
		return airportCode;
	}

	public void setAirportCode(String airportCode) {
		this.airportCode = airportCode;
	}

	public Queue<Flight> getReadyQueue() {
		return readyQueue;
	}

	public void setReadyQueue(Queue<Flight> readyQueue) {
		this.readyQueue = readyQueue;
	}
}
