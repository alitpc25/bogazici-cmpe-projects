import java.util.HashSet;
import java.util.NoSuchElementException;
import java.util.Stack;

public class FactoryImpl implements Factory {
	
	private Holder first;
	private Holder last;
	private Integer size;
	
	public FactoryImpl() {
		first = null;
		last = null;
		size = 0;
	}

	public Holder getFirst() {
		return first;
	}

	public void setFirst(Holder first) {
		this.first = first;
	}

	public Holder getLast() {
		return last;
	}

	public void setLast(Holder last) {
		this.last = last;
	}

	public Integer getSize() {
		return size;
	}

	public void setSize(Integer size) {
		this.size = size;
	}

	@Override
	public void addFirst(Product product) {
		Holder temp = new Holder(null, product, first); // To change with the current head.
		if(size == 0) {
			first = temp;
			last = temp;
		} else {
			first.setPreviousHolder(temp);
			first = temp;
		}
		size++;
	}

	@Override
	public void addLast(Product product) {
		Holder temp = new Holder(last, product, null); // To change with the current tail.
		if(size == 0) {
			first = temp;
			last = temp;
		} else {
			last.setNextHolder(temp);
			last = temp;
		}
		size++;
	}

	@Override
	public Product removeFirst() throws NoSuchElementException {
		if(size == 0) throw new NoSuchElementException();
		Holder temp = first;
		if(size == 1) {
			first = null;
			last = null;
		} else {
			first = first.getNextHolder();
			first.setPreviousHolder(null);
		}
		temp.setNextHolder(null);
		size--;
		return temp.getProduct();
	}

	@Override
	public Product removeLast() throws NoSuchElementException {
		if(size == 0) throw new NoSuchElementException();
		Holder temp = last;
		if(size == 1) {
			first = null;
			last = null;
		} else {
			last = last.getPreviousHolder();
			last.setNextHolder(null);
		}
		temp.setPreviousHolder(null);
		size--;
		return temp.getProduct();
	}

	@Override
	public Product find(int id) throws NoSuchElementException {
		Holder iter = first; // Starts from head and iterates through linkedlist.
		while(iter != null) {
			if(iter.getProduct().getId() == id) {
				break;
			}
			iter = iter.getNextHolder();
		}
		if(iter == null) throw new NoSuchElementException();
		return iter.getProduct();
	}

	@Override
	public Product update(int id, Integer value) throws NoSuchElementException {
		Product product = find(id);
		Product productOldData = new Product(id, product.getValue()); // To print the values before update.
		product.setValue(value);
		return productOldData;
	}

	@Override
	public Product get(int index) throws IndexOutOfBoundsException {
		if(index+1 > size || index < 0) {
			throw new IndexOutOfBoundsException();
		}
		Holder iter = first;
		int count = 0;
		while(count != index) {
			iter = iter.getNextHolder();
			count++;
		}
		return iter.getProduct();
	}

	@Override
	public void add(int index, Product product) throws IndexOutOfBoundsException {
		if(index > size || index < 0) {
			throw new IndexOutOfBoundsException();
		}
		if(index == 0) {
			addFirst(product);
		} else if(index == size) {
			addLast(product);
		} else {
			int count = 0;
			Holder iter = first;
			while(count != index-1) {
				iter = iter.getNextHolder();
				count++;
			}
			// To add between two elements of linkedlist.
			Holder prevHolder = iter;
			Holder nextHolder = iter.getNextHolder();
			Holder toAddHolder = new Holder(prevHolder, product, nextHolder);
			prevHolder.setNextHolder(toAddHolder);
			nextHolder.setPreviousHolder(toAddHolder);
			size++;
		}
	}

	@Override
	public Product removeIndex(int index) throws IndexOutOfBoundsException {
		if(index+1 > size || index < 0) {
			throw new IndexOutOfBoundsException();
		}
		Product removedProduct = null;
		if(index == 0) {
			removedProduct = removeFirst();
		} else if(index == size-1) {
			removedProduct = removeLast();
		} else {
			int count = 0;
			Holder iter = first;
			while(count != index-1) {
				iter = iter.getNextHolder();
				count++;
			}
			// To remove element between two elements of linkedlist.
			Holder prevHolder = iter;
			Holder temp = iter.getNextHolder();
			removedProduct = temp.getProduct();
			Holder nextHolder = temp.getNextHolder();
			prevHolder.setNextHolder(nextHolder);
			nextHolder.setPreviousHolder(prevHolder);
			size--;
		}
		return removedProduct;
	}

	@Override
	public Product removeProduct(int value) throws NoSuchElementException {
		Holder iter = first;
		while(iter != null && iter.getProduct().getValue() != value) {
			iter = iter.getNextHolder();
		}
		if(iter == null) throw new NoSuchElementException();
		if(iter.equals(first)) {
			removeFirst();
		} else if(iter.equals(last)) {
			removeLast();
		} else {
			// To remove element between two elements of linkedlist.
			Holder prevHolder = iter.getPreviousHolder();
			Holder nextHolder = iter.getNextHolder();
			prevHolder.setNextHolder(nextHolder);
			nextHolder.setPreviousHolder(prevHolder);
			size--;
		}
		return iter.getProduct();
	}

	@Override
	public int filterDuplicates() {
		HashSet<Integer> set = new HashSet<>(); // Used set to ensure uniqueness.
		Holder iter = first;
		int duplicatesCount = 0;
		int index = 0;
		while(iter != null) {
			if(!set.contains(iter.getProduct().getValue())) {
				set.add(iter.getProduct().getValue());
				index++;
			} else {
				removeIndex(index);
				duplicatesCount++;
			}
			iter = iter.getNextHolder();
		}
		return duplicatesCount;
	}

	@Override
	public void reverse() {
		Holder iter = first; // To iterate through linkedlist
		Holder prevLast = last; // prevLast will be the new head of linkedlist.
		last = first; // current first becomes new last.
		first = prevLast; // current last becomes new first.
		while(iter != null) {
			Holder oldPrev = iter.getPreviousHolder();
			Holder oldNext = iter.getNextHolder();
			iter.setPreviousHolder(oldNext);
			iter.setNextHolder(oldPrev);
			iter = iter.getPreviousHolder();
		}
	}

	@Override
	public String toString() {
		String result = "{";
		Holder iter = first;
		while(iter != null) {
			result += iter.getProduct();
			iter = iter.getNextHolder();
			if(iter != null) {
				result+=",";
			}
		}
		return result+"}";
	}
}