from typing import List

def getMaxLen(nums: List[int]) -> int:
    current = 1
    ne_len = 0
    cand = 0
    maxi = 0
    temp = 0
    for i in range(0, len(nums)):

        if (nums[i] == 0):
            cand = 0
            ne_len = 0
            current = 1
            temp = 0
        
        elif (nums[i] > 0):
            current *= nums[i]
            if (current > 0):
                cand += 1
        
            else:
                ne_len += 1
                temp += 1
                if (maxi < temp):
                    maxi = temp
        
        else:
            current *= nums[i]
            if (current > 0):
                cand = cand + ne_len + 1
                ne_len = 0
                temp = 0

            else:
                
                ne_len += 1
        
        maxi = max(cand, maxi)
        print("max: ", maxi)
        print("cand: ", cand)
        print("ne_len: ", ne_len)
        print("temp: ", temp)

    return maxi

    
def main():
    print(getMaxLen([5,-20,-20,-39,-5,0,0,0,36,-32,0,-7,-10,-7,21,20,-12,-34,26,2]))

main()