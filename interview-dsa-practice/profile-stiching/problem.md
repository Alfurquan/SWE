# User Identity Stitching
We are building a system to stitch together scattered user identities. You are given a list of profiles. Each profile contains a name as the first element, followed by a list of email addresses associated with that name.

Some users might have created multiple profiles across our platform using different combinations of their emails. If two profiles share at least one email address, we guarantee they belong to the same person.

Task: Write a function to merge these profiles. The output should be a list of merged profiles, where each profile has the name followed by all the unique emails associated with that person, sorted alphabetically.

Example:

Input:
```
profiles = [
    ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
    ["John", "johnsmith@mail.com", "john00@mail.com"],
    ["Mary", "mary@mail.com"],
    ["John", "johnnybravo@mail.com"]
]
```

Output:
```
[
    ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
    ["Mary", "mary@mail.com"],
    ["John", "johnnybravo@mail.com"]
]
```

---

## Approach 

Here is how I would approach the problem. 
First I will reiterate the problem here,
We are given a list of user profiles, where each element in the list is another list whose first element is the name of the user and rest of the elements are email address. We need to merge these user profiles and the output would be list of user profiles where each profile would have a name followed by list of unique email address associated with that person sorted alphabetically.

High level logic
I would approach this problem as a graph problem where I would be building an adjacency list of emails to list of emails connected to it from the input provided.
I would also be using a dictionary to store email to name mapping to quickly look for the name of the person by email address.

I would then loop over all the emails in the adjacency list of emails and perform DFS on it. I would track all visited emails using a visited set. At each DFS call, I would store the email visited in a temporary result set. 
On return from the recursive DFS calls to main for loop, I would be having the temporary result set of emails, I would sort this list, then look up the name of the person using the email on which I am looping over from the dictionary and add the name and the temporary result set of emails to the final result set.

At the the end of looping over all the emails in the adjacency list, I would return the final result set.


## Time and space complexity

Here is how I would be computing the time and space complexity of this approach.

Given -
N: No of profiles
K: Max no of emails in a single profile

Assuming - 
V: No of distinct emails
E: Total No of email connections

Time complexity - 
1. For building the adjacency list, we are looping over all the profiles and all the emails in a profile.
This would be O(N*K)
2. For DFS, we are visiting each email and each connection atmost once, so it would be - O(V + E)
3. Sorting the result set, in worst case all emails would belong to one person, so that would N*K, Sorting that would take O(NK log(NK)
Since sorting dominates the graph building and traversal,
Time complexity = O(NK log(NK)

Space Complexity - 
1. Dictionary to store all email to name mappings - O(V)
2. Adjacency list to store all email connections - O(V + E)
