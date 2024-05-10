import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
// https://leetcode.com/discuss/interview-question/810154/binary-autocomplete

// As each new command is entered, append to the output list the index of the previously entered command that
// share the longest common prefix. If multiple commands are tied, choose the most recent one. If there is no
// previous command that shares a common prefix, output the index of the last command.
class Result {

    /*
     * Complete the 'autocomplete' function below.
     *
     * The function is expected to return an INTEGER_ARRAY.
     * The function accepts STRING_ARRAY command as parameter.
     */

    public static List<Integer> autocomplete(List<String> command) {
    // Write your code here
        int turn = 0;
        ArrayList<ArrayList<Integer>> hs0s = new ArrayList<ArrayList<Integer>>(); // sets of commands with '0's
        ArrayList<ArrayList<Integer>> hs1s = new ArrayList<ArrayList<Integer>>(); // sets of commands with '1's
        ArrayList<Integer> ret = new ArrayList<Integer>();
        
        for (String cmd : command) {
            if (turn == 0) {
                ret.add(0);
            } else {
                // dumb method to loop through all candidates, eliminating as we go
                ArrayList<Integer> cands = new ArrayList<Integer>();   
                for (int i = 0; i < cmd.length(); ++i) {
                    ArrayList<Integer> newCands = new ArrayList<Integer>();
                    int val = (cmd.charAt(i)) - 48;
                    
                    ArrayList<Integer> hs0 = new ArrayList<Integer>();
                    ArrayList<Integer> hs1 = new ArrayList<Integer>();
                    if (i < hs0s.size()) {
                        hs0 = hs0s.get(i);
                    }
                    if (i < hs1s.size()) {
                        hs1 = hs1s.get(i);
                    }
                    if (i == 0) {
                        // check whether the command starts with 0
                        if (val == 0) {
                            for (int elem : hs0) {
                                newCands.add(elem);
                            }
                        } else {
                            for (int elem: hs1) {
                                newCands.add(elem);
                            }
                        }
                        
                    } else {
                        if (val == 0) {
                            for (int cand : cands) {
                                if (hs0.contains((Integer)cand)) {
                                    newCands.add(Integer.valueOf(cand));
                                }
                            }
                        } else {
                            for (int cand : cands) {
                                if (hs1.contains((Integer)cand)) {
                                    newCands.add(Integer.valueOf(cand));
                                }
                            }                            
                        }
                    }
                    switch (newCands.size()) {
                        case 0:
                            // use previous candidates(!!)
                            if (cands.size() == 0) {
                                ret.add(turn);
                            } else {
                                ret.add(cands.get(cands.size() - 1));
                            }
                            break;
                        case 1:
                            ret.add(newCands.get(0));
                            break;
                        default: // continue with the loop
                    }
                    if (newCands.size() <= 1) {
                        break;
                    }
                    cands = newCands;
                }
            }
            // now add this new command to hs0s and hs1s
            for (int i = 0; i < cmd.length(); ++i) {
                int val = (cmd.charAt(i)) - 48;
                if (val == 0) {
                    if (i < hs0s.size()) {
                        ArrayList<Integer> hs0 = hs0s.get(i);
                        hs0.add(turn + 1);
                    } else {
                        ArrayList<Integer> n = new ArrayList<Integer>();
                        n.add(turn + 1);
                        hs0s.add(n);
                    }
                    while (hs1s.size() <= i) {
                        hs1s.add(new ArrayList<Integer>());
                    }
                    
                } else {
                    if (i < hs1s.size()) {
                        ArrayList<Integer> hs1 = hs1s.get(i);
                        hs1.add(turn + 1);
                    } else {
                        ArrayList<Integer> n = new ArrayList<Integer>();
                        n.add(turn + 1);
                        hs1s.add(n);
                    }
                    while (hs0s.size() <= i) {
                        hs0s.add(new ArrayList<Integer>());
                    }
                }
                                        
            }
            // System.out.println("hs0s");
            // dbg(hs0s);
            // System.out.println("hs1s");
            // dbg(hs1s);
            ++turn;
        }
        return ret;
    }

    public static void dbg(ArrayList<ArrayList<Integer>> ans) {
        for (int i = 0; i < ans.size(); ++i) {
            var arr = ans.get(i);
            System.out.print("\t" + i + ": ");
            for (var elem: arr) {
                System.out.print(elem + " ");
            }
            System.out.println();
        }
    }
    public static void main(String[] args) {
        // List<String> test = Arrays.asList(new String[] {"10111", "1011001"}); 
        List<String> test = Arrays.asList(new String[] {"10111", "1011001", "01001", "110001"});
        List<Integer> res = autocomplete(test);
        for (int ans: res) {
            System.out.println(ans);
        }
    }

}