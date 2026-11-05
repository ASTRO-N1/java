import java.util.*;

public class Alpha{
    static char counter = 'A';

    static class Node{
        int depth, value;
        boolean isMax, pruned = false;
        char name;
        Node left, right;

        Node(int depth, boolean isMax){
            this.depth = depth;
            this.isMax = isMax;
        }
    }

    static Node buildTree (int depth, int[] leaves, int index, boolean isMax){
        Node node = new Node(depth, isMax);
        node.name = counter++;

        if (depth==0){
            node.value = leaves[index];
            return node;
        }

        node.left = buildTree(depth-1, leaves, index * 2, !isMax);
        node.right = buildTree(depth-1, leaves, index * 2 + 1 , !isMax);
        return node;
    
    }

    static int alphaBeta (Node node, int alpha, int beta){
        if (node.depth == 0){
            return node.value;
        }

        if(node.isMax){
            int best = Integer.MIN_VALUE;
            best = Math.max(best, alphaBeta(node.left, alpha, beta));
            alpha = Math.max(alpha, best);

            if (alpha >= beta){
                node.right.pruned = true;
            }else{
                best = Math.max(best, alphaBeta(node.right, alpha, beta));  
            }
            node.value = best;
            return best;
        }else{
            int best = Integer.MAX_VALUE;
            best = Math.min(best, alphaBeta(node.left, alpha, beta));
            beta = Math.min(beta, best);

            if (alpha >= beta){
                node.right.pruned = true;
            }else{
                best = Math.min(best, alphaBeta(node.right, alpha, beta));  
            }
            node.value = best;
            return best;
        }
        
    }

    static void display(Node node, String prefix, boolean isLast, boolean root){

        if (node.pruned){
            String branch = isLast ? "'--" : "|--";
            System.out.println(prefix + branch + node.name + " ( pruned ) ");
            return;
        }

        if(root){
            System.out.println("Root " + node.name + " (max) " + node.value );
        }else{
            String branch = isLast ? "'--" : "|--";
            System.out.println(prefix + branch + node.name + );
        }
    }
}