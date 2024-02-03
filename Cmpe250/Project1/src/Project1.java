import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.NoSuchElementException;
import java.util.Scanner;

public class Project1 {
	
	public static FactoryImpl factoryImpl = new FactoryImpl();
	
	public static void main(String[] args) {
		try {
		File readObject = new File(args[0]); // args[0] = input dir
		    Scanner myReader = new Scanner(readObject);
		    FileWriter myWriter = new FileWriter(args[1]); // args[1] = output dir
		    while (myReader.hasNextLine()) {
		        String[] data = myReader.nextLine().split(" ");
		        executeAndWriteByCommand(data, myWriter);
		    }
		    myReader.close();
		    myWriter.close();
		} catch (IOException e) {
		    e.printStackTrace();
		}
	}
	
	// Method to write given data to the output file.
	public static void writeToOutput(FileWriter myWriter, String dataToWrite) {
		try {
			myWriter.write(dataToWrite+"\n");
		} catch(IOException ioException) {
			ioException.printStackTrace();
		}
	}
	
	public static void executeAndWriteByCommand(String[] data, FileWriter myWriter) {
		Product product;
		switch(data[0]) {
			case "AF":
				product = new Product(Integer.valueOf(data[1]), Integer.valueOf(data[2]));
				factoryImpl.addFirst(product);
				break;
			case "AL":
				product = new Product(Integer.valueOf(data[1]), Integer.valueOf(data[2]));
				factoryImpl.addLast(product);
				break;
			case "A":
				product = new Product(Integer.valueOf(data[2]), Integer.valueOf(data[3]));
				try {
					factoryImpl.add(Integer.valueOf(data[1]), product);
				} catch(IndexOutOfBoundsException e) {
					writeToOutput(myWriter, "Index out of bounds.");
				}
				break;
			case "RF":
				try {
					product = factoryImpl.removeFirst();
					writeToOutput(myWriter, product.toString());
				} catch(NoSuchElementException e) {
					writeToOutput(myWriter, "Factory is empty.");
				}
				break;
			case "RL":
				try {
					product = factoryImpl.removeLast();
					writeToOutput(myWriter, product.toString());
				} catch(NoSuchElementException e) {
					writeToOutput(myWriter, "Factory is empty.");
				}
				break;
			case "RI":
				try {
					product = factoryImpl.removeIndex(Integer.valueOf(data[1]));
					writeToOutput(myWriter, product.toString());
				} catch(IndexOutOfBoundsException e) {
					writeToOutput(myWriter, "Index out of bounds.");
				}
				break;
			case "RP":
				try {
					product = factoryImpl.removeProduct(Integer.valueOf(data[1]));
					writeToOutput(myWriter, product.toString());
				} catch(NoSuchElementException e) {
					writeToOutput(myWriter, "Product not found.");
				}
				break;
			case "F":
				try {
					product = factoryImpl.find(Integer.valueOf(data[1]));
					writeToOutput(myWriter, product.toString());
				} catch(NoSuchElementException e) {
					writeToOutput(myWriter, "Product not found.");
				}
				break;
			case "G":
				try {
					product = factoryImpl.get(Integer.valueOf(data[1]));
					writeToOutput(myWriter, product.toString());
				}  catch(IndexOutOfBoundsException e) {
					writeToOutput(myWriter, "Index out of bounds.");
				}
				break;
			case "U":
				try {
					product = factoryImpl.update(Integer.valueOf(data[1]), Integer.valueOf(data[2]));
					writeToOutput(myWriter, product.toString());
				} catch(NoSuchElementException e) {
					writeToOutput(myWriter, "Product not found.");
				}
				break;
			case "FD":
				int i = factoryImpl.filterDuplicates();
				writeToOutput(myWriter, String.valueOf(i));
				break;
			case "R":
				factoryImpl.reverse();
				writeToOutput(myWriter, factoryImpl.toString());
				break;
			case "P":
				writeToOutput(myWriter, factoryImpl.toString());
				break;
		}
	}
}