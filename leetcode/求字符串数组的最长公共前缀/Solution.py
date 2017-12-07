class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ""
        if len(strs) == 1:
            return strs[0]
        i = 0 
        while True:
            continuos = True
            for ind in range(0, len(strs)-1):
                if i >= len(strs[ind]) or i >= len(strs[ind+1]):
                    continuos = False
                    break
                if strs[ind][i] != strs[ind+1][i]:
                    continuos = False
                    break
            if not continuos:
                break
            i = i + 1 
        return strs[0][:i]