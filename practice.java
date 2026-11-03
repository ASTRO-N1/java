import java.util.*;

public class practice {
    static char counter = 'A';

     static class Node {
        int depth, value;
        boolean isMax, pruned = false;
        Node left , right;
        char name;

        Node(int depth, boolean isMax){
            this.depth = depth;
            this.isMax = isMax;
        }

    }

    static Node buildTree(int depth,int[] leaves,int index,boolean isMax){
        Node node = new Node(depth,isMax);
        node.name = counter++;

        if(depth == 0){
            node.value = leaves[index];
            return node;
        }

        node.left = buildTree(depth-1,leaves,index*2,!isMax);
        node.right = buildTree(depth-1,leaves,index*2 + 1,!isMax);

        return node;
    }

    static int alphaBeta(Node node, int alpha, int beta) {
        if (node.depth == 0) {
            return node.value;
        }

        if (node.isMax) {
            int best = Integer.MIN_VALUE;
            best = Math.max(best, alphaBeta(node.left, alpha, beta));
            alpha = Math.max(alpha, best);


            if (alpha >= beta) {
                node.right.pruned = true;
            } else {
                best = Math.max(best, alphaBeta(node.right, alpha, beta));
            }

            node.value = best;
            return best;

        }else{
            int best = Integer.MAX_VALUE;
            best = Math.min(best, alphaBeta(node.left,alpha,beta) );
            beta = Math.min(best,beta);

            if(alpha >= beta){
                node.right.pruned = true;
            }else{
                best = Math.min(best, alphaBeta(node.right,alpha,beta) );
            }
            node.value = best;
            return best;
        }

    }


    static void display(Node node, String prefix, boolean isLast, boolean root) {

        if (node.pruned) {
            String branch = isLast ? "'-- " : "|-- ";
            System.out.println(prefix + branch + node.name + " (pruned) ");
            return;
        }

        if (root) {
            System.out.println("Root " + node.name +" (max) : "  + node.value);
        } else {
            String branch = isLast ? "'-- " : "|-- ";

            if (node.depth == 0) {
                System.out.println(prefix + branch + node.name +" : " + node.value + " (leaf)");
            } else {
                String type = node.isMax ? "max" : "min";
                System.out.println(prefix + branch + node.name + "("+type+")"+ ": " + node.value);
            }
        }

        if (node.depth > 0) {

            String newPrefix;

            if (root) {
                newPrefix = "";
            } else {
                newPrefix = prefix + (isLast ? "    " : "|   ");
            }

            display(node.left, newPrefix, false, false);
            display(node.right, newPrefix, true, false);
        }
    }

    static void printPath(Node node){
         if(node.depth == 0){
             System.out.println(node.name);
             return;
         }
         System.out.print((node.name) +  " -> ");
         Node next;

         if(!node.left.pruned && node.left.value == node.value){
             next = node.left;
         }
         else{
             next = node.right;
         }

         printPath(next);

    }


    public static void main(String[] args) {

         Scanner sc = new Scanner(System.in);

         System.out.print("Enter depth : ");
         int depth = sc.nextInt();

         int size = (int) Math.pow(2,depth);   //type casting

         System.out.println("Enter " + size + " values:");

         int[] leaves = new int[size];

         for(int i = 0; i < size; i++){
             leaves[i] = sc.nextInt();
         }

        counter = 'A';
        Node root = buildTree(depth, leaves, 0, true);

        int result = alphaBeta(root,
                Integer.MIN_VALUE, Integer.MAX_VALUE);

        System.out.println("\nGame Tree:");

        display(root, "", true, true);

        System.out.println("\nOptimal Value: " + result);

        System.out.println("\nOptimal Path:");
        printPath(root);
        
        sc.close();
    }

}
