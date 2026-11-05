import java.util.*;

public class AlphaBeta {
    static int[] leaves;
    static int b, d;
    static final int INF = 1000000;

    static int ab(int depth, int idx, boolean isMax, int alpha, int beta) {
        String pad = "    ".repeat(depth);          // indentation = tree level

        if (depth == d) {                           // leaf node
            System.out.println(pad + "Leaf = " + leaves[idx]);
            return leaves[idx];
        }

        System.out.println(pad + (isMax ? "MAX" : "MIN") + "  alpha=" + alpha + " beta=" + beta);
        int best = isMax ? -INF : INF;

        for (int i = 0; i < b; i++) {
            int val = ab(depth + 1, idx * b + i, !isMax, alpha, beta);

            if (isMax) {
                best = Math.max(best, val);
                alpha = Math.max(alpha, best);
            } else {
                best = Math.min(best, val);
                beta = Math.min(beta, best);
            }

            if (alpha >= beta) {                    // pruning condition
                if (i < b - 1)
                    System.out.println(pad + "  PRUNED " + (b - 1 - i) + " remaining branch(es)");
                break;
            }
        }
        System.out.println(pad + "=> value=" + best + " (alpha=" + alpha + ", beta=" + beta + ")");
        return best;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Branching factor: ");
        b = sc.nextInt();
        System.out.print("Depth: ");
        d = sc.nextInt();

        int n = (int) Math.pow(b, d);
        leaves = new int[n];
        System.out.println("Enter " + n + " leaf values:");
        for (int i = 0; i < n; i++) leaves[i] = sc.nextInt();

        int result = ab(0, 0, true, -INF, INF);
        System.out.println("\nFinal answer (root value) = " + result);
    }
}