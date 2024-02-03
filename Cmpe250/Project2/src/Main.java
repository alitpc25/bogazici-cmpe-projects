import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class Main {
	public static BinarySearchTree bstree;
	public static AVLTree avltree;
	public static void main(String[] args) {
		try {
		File readObject = new File(args[0]); // args[0] = input dir
		    Scanner myReader = new Scanner(readObject);
		    FileWriter myWriterBst = new FileWriter(args[1]+"_bst.txt");
		    FileWriter myWriterAvl = new FileWriter(args[1]+"_avl.txt");
		    String initialRootIpAddress = myReader.nextLine();
		    avltree = new AVLTree(initialRootIpAddress, myWriterAvl);
		    bstree = new BinarySearchTree(initialRootIpAddress, myWriterBst);
		    while (myReader.hasNextLine()) {
		        String[] data = myReader.nextLine().split(" ");
		        executeAndWriteByCommand(data);
		    }
		    myReader.close();
		    myWriterBst.close();
		    myWriterAvl.close();
		} catch (IOException e) {
		    e.printStackTrace();
		}
	}
	
	public static void executeAndWriteByCommand(String[] data) {
		switch(data[0]) {
		case "ADDNODE":
			avltree.insert(data[1]);
			bstree.insert(data[1]);
			break;
		case "DELETE":
			avltree.remove(data[1]);
			bstree.remove(data[1]);
			break;
		case "SEND":
			avltree.sendMessage(data[1], data[2]);
			bstree.sendMessage(data[1], data[2]);
			break;
		}
	}
}
