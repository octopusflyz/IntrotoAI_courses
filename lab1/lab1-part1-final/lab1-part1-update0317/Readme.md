 
修改版本 
意识到第一版虽然可以通过所有样例测试。 
但是UCS 和A星处对priority_queue key部分的冗余使用，导致将维护一个非常大的堆，或许对于样例小样本还行，大样例极有可能崩掉。 
于是修改两处的key均只针对position，而用另外的dictionary来存储action。 
此处改动又进而引起了cornersproblem的state不可哈希使用dictionary的问题。 
于是又魔改了部分searchAgents中cornersProblem类中的函数，强制将所有类转换为tuple形式。 
希望这些改动是允许的。/(ㄒoㄒ)/
