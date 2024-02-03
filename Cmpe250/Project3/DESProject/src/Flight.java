import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Flight {
	private String flightCode;
	private int state;
	private ATC departureAirport;
	private ATC landingAirport;
	private ACC acc;
	private long updateTime;
	private long addingTimeToACCQueue;
	private long addingTimeToATCQueue;
	private boolean isSentBackToTheACCQueue;
	
	public boolean isSentBackToTheACCQueue() {
		return isSentBackToTheACCQueue;
	}

	public void setSentBackToTheACCQueue(boolean isSentBackToTheACCQueue) {
		this.isSentBackToTheACCQueue = isSentBackToTheACCQueue;
	}

	public long getAddingTimeToACCQueue() {
		return addingTimeToACCQueue;
	}

	public void setAddingTimeToACCQueue(long addingTimeToACCQueue) {
		this.addingTimeToACCQueue = addingTimeToACCQueue;
	}
	
	public long getAddingTimeToATCQueue() {
		return addingTimeToATCQueue;
	}

	public void setAddingTimeToATCQueue(long addingTimeToATCQueue) {
		this.addingTimeToATCQueue = addingTimeToATCQueue;
	}

	//Has 21 operation steps (certain form) to complete before termination.
	private long admissionTime;
	private List<Integer> operations;

	public Flight(String flightCode, int state, ATC departureAirport, ATC landingAirport, ACC acc,
			int admissionTime) {
		this.flightCode = flightCode;
		this.state = state;
		this.departureAirport = departureAirport;
		this.landingAirport = landingAirport;
		this.acc = acc;
		this.admissionTime = admissionTime;
		this.operations = new ArrayList<Integer>();
	}

	public long getUpdateTime() {
		return updateTime;
	}

	public void setUpdateTime(long updateTime) {
		this.updateTime = updateTime;
	}

	public int getState() {
		return state;
	}

	public void setState(int state) {
		this.state = state;
	}
	
	public String getFlightCode() {
		return flightCode;
	}

	public void setFlightCode(String flightCode) {
		this.flightCode = flightCode;
	}

	public ATC getDepartureAirport() {
		return departureAirport;
	}

	public void setDepartureAirport(ATC departureAirport) {
		this.departureAirport = departureAirport;
	}

	public ATC getLandingAirport() {
		return landingAirport;
	}

	public void setLandingAirport(ATC landingAirport) {
		this.landingAirport = landingAirport;
	}

	public ACC getAcc() {
		return acc;
	}

	public void setAcc(ACC acc) {
		this.acc = acc;
	}

	public long getAdmissionTime() {
		return admissionTime;
	}

	public void setAdmissionTime(long admissionTime) {
		this.admissionTime = admissionTime;
	}

	public List<Integer> getOperations() {
		return operations;
	}

	public void setOperations(List<Integer> operations) {
		this.operations = operations;
	}
	
}

class FlightComparator implements Comparator<Flight>{
	@Override
	public int compare(Flight o1, Flight o2) {
		if(o1.getAddingTimeToACCQueue() != o2.getAddingTimeToACCQueue()) {
			return (int) (o1.getAddingTimeToACCQueue() - o2.getAddingTimeToACCQueue());
		}
		if(o1.isSentBackToTheACCQueue() && !o2.isSentBackToTheACCQueue()) {
			return 1;
		}
		if(!o1.isSentBackToTheACCQueue() && o2.isSentBackToTheACCQueue()) {
			return -1;
		}
		return o1.getFlightCode().compareTo(o2.getFlightCode());
	}
}

class FlightComparatorWait implements Comparator<Flight>{
	@Override
	public int compare(Flight o1, Flight o2) {
		return o1.getOperations().get(0) - o2.getOperations().get(0);
	}
}

class FlightComparatorAtc implements Comparator<Flight>{
	@Override
	public int compare(Flight o1, Flight o2) {
		if(o1.getAddingTimeToATCQueue() != o2.getAddingTimeToATCQueue()) {
			return (int) (o1.getAddingTimeToATCQueue() - o2.getAddingTimeToATCQueue());
		}
		return o1.getFlightCode().compareTo(o2.getFlightCode());
	}
}