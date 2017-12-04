public class DropEggs {
    public static void dropEggs(int height, int point, int jump) {
        jump = height / jump;
        for (int i = 0, firstEggHeight; (firstEggHeight = i * jump) <= height; i++) {
            firstEggHeight = firstEggHeight + jump;
            System.out.println(String.format("从%3d层仍第一个鸡蛋", firstEggHeight));
            if (firstEggHeight < point)
                continue;
            System.out.println("第一个鸡蛋碎了，开始仍第二个鸡蛋");
            for (int j = 0, secondEggHeight;
                    (secondEggHeight =  firstEggHeight - jump + 1 + j) <= point; j++) {
                System.out.println(String.format("从%3d层仍第二个鸡蛋", secondEggHeight));
                if (secondEggHeight == point)
                    System.out.println("第二个鸡蛋碎了, 总共扔了" + (i + j + 2) + "次");
            }
            
            break;
        }

    }

    public static void main(String[] args) {
        dropEggs(95, 80, 10);
    }
}
