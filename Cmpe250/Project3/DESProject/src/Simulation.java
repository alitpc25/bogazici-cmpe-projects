import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.PriorityQueue;

public class Simulation {
	private ACC acc;
	private List<ATC> atcList;
	private PriorityQueue<Flight> flights;
	private long clock;
	private int finishedFlights = 0;
	private int flightCount;
	private List<Flight> waitingAccFlights = new ArrayList<>();
	private List<Flight> waitingAtcFlights = new ArrayList<>();
	private long timeToUpdateAccQueue;
	
	public int getFinishedFlights() {
		return finishedFlights;
	}

	public void setFinishedFlights(int finishedFlights) {
		this.finishedFlights = finishedFlights;
	}

	public int getFlightCount() {
		return flightCount;
	}

	public void setFlightCount(int flightCount) {
		this.flightCount = flightCount;
	}

	public Simulation(ACC acc, List<ATC> atcList, PriorityQueue<Flight> flights, long clock, int flightCount) {
		this.acc = acc;
		this.atcList = atcList;
		this.flights = flights;
		this.clock = clock;
		this.flightCount = flightCount;
	}

	public ACC getAcc() {
		return acc;
	}

	public void setAcc(ACC acc) {
		this.acc = acc;
	}

	public List<ATC> getAtcList() {
		return atcList;
	}

	public void setAtcList(List<ATC> atcList) {
		this.atcList = atcList;
	}

	public PriorityQueue<Flight> getFlights() {
		return flights;
	}

	public void setFlights(PriorityQueue<Flight> flights) {
		this.flights = flights;
	}

	public long getClock() {
		return clock;
	}

	public void setClock(long clock) {
		this.clock = clock;
	}
	
	private void updateAccQueue() {
		if(acc.getReadyQueue().peek() != null) {
			Flight f = acc.getReadyQueue().poll();
			f.setAddingTimeToACCQueue(clock);
			f.setSentBackToTheACCQueue(true);
			acc.getReadyQueue().add(f);
		}
		timeToUpdateAccQueue = clock+30;
	}

	public String start() {
		timeToUpdateAccQueue = clock+30;
		while(finishedFlights < flightCount) {
			while(flights.peek() != null && flights.peek().getAdmissionTime() == clock) {
				Flight f = flights.poll();
    			f.setAddingTimeToACCQueue(clock);
    			if(acc.getReadyQueue().isEmpty()) {
	    			timeToUpdateAccQueue = clock+30;
	    		}
    			f.setSentBackToTheACCQueue(false);
    			acc.getReadyQueue().add(f);
			}
			
			long minAccProcessTime = 30;
			long minAtcProcessTime = 30;
			long minWaitTime = 30;
			if(acc.getReadyQueue().size()>0)
				minAccProcessTime = Math.min(minAccProcessTime, acc.getReadyQueue().peek().getOperations().get(0));
			for(ATC atc : atcList) {
				if(atc.getReadyQueue().size() > 0) {
					minAtcProcessTime = Math.min(minAtcProcessTime, atc.getReadyQueue().peek().getOperations().get(0));
				}
			}
			if(waitingAtcFlights.size()>0) {
				for(Flight f : waitingAtcFlights) {
					minWaitTime = Math.min(f.getOperations().get(0), minWaitTime);
				}
			}
			if(waitingAccFlights.size()>0) {
				for(Flight f : waitingAccFlights) {
					minWaitTime = Math.min(f.getOperations().get(0), minWaitTime);
				}
			}
			long minProgress = Math.min(timeToUpdateAccQueue-clock, minAccProcessTime);
			minProgress = Math.min(minProgress, minAtcProcessTime);
			minProgress = Math.min(minProgress, minWaitTime);
			if(flights.size() > 0)
				minProgress = Math.min(minProgress, flights.peek().getAdmissionTime() - clock);
			handleACCRun(minProgress);
			handleACCWait(minProgress);
			handleATCRun(minProgress);
			handleATCWait(minProgress);
			tickClock(minProgress);
			//System.out.println(clock);
			if(timeToUpdateAccQueue == clock) {
				updateAccQueue();
			}
		}
		List<String> airports = new ArrayList<>();
		List<Integer> keySet = acc.getHashTable().getKeySet();
    	Collections.sort(keySet);
    	for(int ind : keySet) {
    		if(!airports.contains(acc.getHashTable().getByIndex(ind).getAirportCode() + String.format("%03d" ,ind))) {
    			airports.add(acc.getHashTable().getByIndex(ind).getAirportCode() + String.format("%03d" ,ind));
    		}
    	}
    	String strAirports = Arrays.toString(airports.toArray()).replace("[", "").replace("]", "").replace(",", "");
    	return acc.getAccCode() + " " + clock + " " + strAirports +"\n";
	}
	
	public void tickClock(long minProgress) {
		clock+=minProgress;
	}
	
	public void handleACCRun(long minProgress) {
		Flight processedFly;
		if(!acc.getReadyQueue().isEmpty()) {
			processedFly = acc.getReadyQueue().peek();
			switch(processedFly.getState()) {
				case 1:
				case 3:
				case 11:
				case 13:
				case 21:
					int opTime = processedFly.getOperations().get(0) - (int) minProgress;
					if(minProgress != 0) {
						processedFly.setUpdateTime(clock);
						processedFly.getOperations().set(0, opTime);
					}
					if(opTime < 1) {
						processedFly.getOperations().remove(0);
						processedFly.setState(processedFly.getState()+1);
						timeToUpdateAccQueue = clock+30+minProgress;
					    processedFly.setSentBackToTheACCQueue(false);
			    	}
					
					if(processedFly.getState() == 4) {
						processedFly.setAddingTimeToATCQueue(clock+minProgress);
						if(!atcList.contains(processedFly.getDepartureAirport())) {
			    			atcList.add(processedFly.getDepartureAirport());
			    		}
						processedFly.getDepartureAirport().getReadyQueue().add(acc.getReadyQueue().poll());
					} else if(processedFly.getState() == 14) {
						processedFly.setAddingTimeToATCQueue(clock+minProgress);
						if(!atcList.contains(processedFly.getLandingAirport())) {
			    			atcList.add(processedFly.getLandingAirport());
			    		}
						processedFly.getLandingAirport().getReadyQueue().add(acc.getReadyQueue().poll());
					} else if(processedFly.getState() == 22) {
						finishedFlights++;
						acc.getReadyQueue().poll();
					} else if(processedFly.getState() == 2 || processedFly.getState() == 12) {
						waitingAccFlights.add(acc.getReadyQueue().poll());
					}
					break;
			}
		}
	}

	public void handleATCRun(long minProgress) {
		for(ATC atc : atcList) {
    		if(!atc.getReadyQueue().isEmpty()) {
    			Flight f = atc.getReadyQueue().peek();
    			if(f.getUpdateTime() < clock) {
    				int opTime;
    				switch(f.getState()) {
	    				case 4:
	    				case 6:
	    				case 8:
	    				case 10:
	    				case 14:
	    				case 16:
	    				case 18:
	    				case 20:
	        				opTime = f.getOperations().get(0) - (int) minProgress;
	        				if(minProgress != 0) {
	    						f.setUpdateTime(clock);
	    						f.getOperations().set(0, opTime);
	        				}
	        		    	if(opTime < 1) {
	        		    		//System.out.println(acc.getAccCode() + " | " + atc.getAirportCode() + " | " + (clock+minProgress) +" | " + f.getFlightCode());
	        		    		f.setState(f.getState()+1);
	        		    		f.getOperations().remove(0);
	    			    	}
	        		    	if(f.getState() == 11 || f.getState() == 21) {
	        		    		f.setAddingTimeToACCQueue(clock+minProgress);
	        		    		if(acc.getReadyQueue().isEmpty()) {
	        		    			timeToUpdateAccQueue = clock+30+minProgress;
	        		    		}
	        		    		f.setSentBackToTheACCQueue(false);
	        		    		acc.getReadyQueue().add(atc.getReadyQueue().poll());
							} else if(f.getState() == 5 || f.getState() == 7 || f.getState() == 9 || f.getState() == 15 || f.getState() == 17 || f.getState() == 19) {
								waitingAtcFlights.add(atc.getReadyQueue().poll());
							}
	    					break;
    				}
    			} 
			}
    	}
	}
	
	public void handleACCWait(long minProgress) {
		for (Iterator<Flight> it = waitingAccFlights.iterator(); it.hasNext(); ) {
		    Flight f = it.next();
		    if(f.getUpdateTime() < clock) {
		    	int opTime = f.getOperations().get(0) - (int) minProgress;
		    	if(minProgress != 0) {
					f.setUpdateTime(clock);
					f.getOperations().set(0, opTime);
		    	}
		    	if(opTime < 1) {
		    		f.setState(f.getState()+1);
		    		f.getOperations().remove(0);
		    		f.setAddingTimeToACCQueue(clock+minProgress);
		    		f.setSentBackToTheACCQueue(false);
		    		if(acc.getReadyQueue().isEmpty()) {
		    			timeToUpdateAccQueue = clock+30+minProgress;
		    		}
    				acc.getReadyQueue().add(f);
    				it.remove();
				}
			}
		}
	}

	public void handleATCWait(long minProgress) {
		for (Iterator<Flight> it = waitingAtcFlights.iterator(); it.hasNext(); ) {
		    Flight f = it.next();
		    if(f.getUpdateTime() < clock) {
		    	int opTime = f.getOperations().get(0) - (int) minProgress;
		    	if(minProgress != 0) {
					f.setUpdateTime(clock);
					f.getOperations().set(0, opTime);
		    	}
		    	if(opTime < 1) {
		    		f.setState(f.getState()+1);
		    		f.setAddingTimeToATCQueue(clock+minProgress);
		    		f.getOperations().remove(0);
		    		if(f.getState() == 6 || f.getState() == 8 || f.getState() == 10) {
		    			if(!atcList.contains(f.getDepartureAirport())) {
			    			atcList.add(f.getDepartureAirport());
			    		}
		    			f.getDepartureAirport().getReadyQueue().add(f);
		    		} else {
		    			if(!atcList.contains(f.getLandingAirport())) {
			    			atcList.add(f.getLandingAirport());
			    		}
		    			f.getLandingAirport().getReadyQueue().add(f);
		    		}
		    		it.remove();
				}
			}
		}
	}
}
