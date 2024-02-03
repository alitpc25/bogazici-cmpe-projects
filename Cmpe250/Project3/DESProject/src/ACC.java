import java.util.PriorityQueue;
import java.util.Queue;

public class ACC {
	// ACC is the entry and exit point for flights.
	// Id: Unique code 4 capital letters.
	private String accCode;
	private Queue<Flight> readyQueue; //ready to be processed by ACC
	private LinearProbingHashTable hashTable;
	
	public ACC(String accCode) {
		this.accCode = accCode;
		this.readyQueue = new PriorityQueue<>(new FlightComparator());
		this.hashTable = new LinearProbingHashTable();
	}
	
	public Queue<Flight> getReadyQueue() {
		return readyQueue;
	}
	public void setReadyQueue(Queue<Flight> readyQueue) {
		this.readyQueue = readyQueue;
	}
	public LinearProbingHashTable getHashTable() {
		return hashTable;
	}
	public void setHashTable(LinearProbingHashTable hashTable) {
		this.hashTable = hashTable;
	}
	public String getAccCode() {
		return accCode;
	}
	public void setAccCode(String accCode) {
		this.accCode = accCode;
	}
	
}