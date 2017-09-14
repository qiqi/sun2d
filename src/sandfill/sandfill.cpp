#include<iostream>
#include<fstream>
#include<string>
#include<vector>

#include"argparse.hpp"

struct Edge {
    int i, j;
    Edge(int i, int j) : i(i), j(j) {}
};

std::vector<Edge> read_input(std::string inputfile)
{
    std::vector<Edge> edges;
    std::ifstream f(inputfile);
    while (!f.eof())
    {
        int i, j;
        if (f >> i >> j) {
            std::cout << i << " " << j << std::endl;
            edges.emplace_back(i, j);
        }
        else {
            break;
        }
    }
    f.close();
    return edges;
}

int main(int argc, const char ** argv)
{
    ArgumentParser parser;
    parser.addArgument("--inputfile", 1, false);
    parser.addArgument("--output_dir", 1, false);
    parser.parse(argc, argv);

    auto edges = read_input(parser.retrieve<std::string>("inputfile"));

    auto output_dir = parser.retrieve<std::string>("output_dir");
    std::cout << output_dir << std::endl;

    return 0;
}
