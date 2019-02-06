#include<iostream>
#include<queue>
#include<string>
#include<sstream>
#include<cstring>
#include<cctype> //for sprintf()
#include<unordered_map>
#include<fstream>
#include<stdlib.h>
#include<streambuf>
#include<stdio.h> 
#include<string.h> 
#include<stdexcept>
#include<iomanip>
#include<bits/stdc++.h> 
#include<zlib.h>

using namespace std;

//Compression of string
std::string compress_string(const std::string& str,int compressionlevel = Z_BEST_COMPRESSION)
{
    z_stream zs;                        // z_stream is zlib's control structure
    memset(&zs, 0, sizeof(zs));

    if (deflateInit(&zs, compressionlevel) != Z_OK)
        throw(std::runtime_error("deflateInit failed while compressing."));

    zs.next_in = (Bytef*)str.data();
    zs.avail_in = str.size();           // set the z_stream's input

    int ret;
    char outbuffer[32768];
    std::string outstring;

    // retrieve the compressed bytes blockwise
    do {
        zs.next_out = reinterpret_cast<Bytef*>(outbuffer);
        zs.avail_out = sizeof(outbuffer);

        ret = deflate(&zs, Z_FINISH);

        if (outstring.size() < zs.total_out) {
            // append the block to the output string
            outstring.append(outbuffer,zs.total_out - outstring.size());
        }
    } while (ret == Z_OK);

    deflateEnd(&zs);

    if (ret != Z_STREAM_END) {          // an error occurred that was not EOF
        std::ostringstream oss;
        oss << "Exception during zlib compression: (" << ret << ") " << zs.msg;
        throw(std::runtime_error(oss.str()));
    }

    return outstring;
}

//Decompress of string
std::string decompress_string(const std::string& str)
{
    z_stream zs;                        // z_stream is zlib's control structure
    memset(&zs, 0, sizeof(zs));

    if (inflateInit(&zs) != Z_OK)
        throw(std::runtime_error("inflateInit failed while decompressing."));

    zs.next_in = (Bytef*)str.data();
    zs.avail_in = str.size();

    int ret;
    char outbuffer[32768];
    std::string outstring;

    // get the decompressed bytes blockwise using repeated calls to inflate
    do {
        zs.next_out = reinterpret_cast<Bytef*>(outbuffer);
        zs.avail_out = sizeof(outbuffer);

        ret = inflate(&zs, 0);

        if (outstring.size() < zs.total_out) {
            outstring.append(outbuffer,zs.total_out - outstring.size());
        }

    } while (ret == Z_OK);

    inflateEnd(&zs);

    if (ret != Z_STREAM_END) {          // an error occurred that was not EOF
        std::ostringstream oss;
        oss << "Exception during zlib decompression: (" << ret << ") " << zs.msg;
        throw(std::runtime_error(oss.str()));
    }

    return outstring;
}

//String Functions
string encrypt(string msg, string const& key)
    {
        if(!key.size())
            return msg;
        
        for (string::size_type i = 0; i < msg.size(); ++i)
            msg[i] ^= key[i % key.size()];
        return msg;
    }
    
string decrypt(string const& msg, string const& key)
    {
        return encrypt(msg, key); 
    }



int main()
{
  std::string ky = "Piepiper";
  std::ifstream t("test.exe",std::ios::binary);
  //Taking file binary and adding it to string
	std::string str((std::istreambuf_iterator<char>(t)),std::istreambuf_iterator<char>());
	std::cout << str.std::string::size() << std::endl;
	std::cout << str.std::string::size() / 2 << std::endl;
  std::string::size_type cols = str.std::string::size() / 2;
  //spitting string into two halfs to preform middle out compression
  std::string half = str.substr(0, str.length()/2);
  std::string otherHalf = str.substr(str.length()/2);
  //Test if data can be mirrored and outputed correctly
	std::ofstream myfile("test2.exe",std::ios::binary);
  if(myfile.is_open())
      {
        myfile << str << std::endl;
      }
	std::ofstream myfile2("test3.exe",std::ios::binary);
  if(myfile2.is_open())
      {
      	myfile2 << half+otherHalf << std::endl;
      }
  //compressing file
  std::string h = encrypt(half,ky);
  std::string h2 = encrypt(otherHalf,ky);
  std::ofstream myfile3("test4.exe",std::ios::binary);
  if(myfile3.is_open())
    {
      myfile3 << h+h2 << std::endl;
    }
  sleep(1);
  //Decompressing compressed file
  std::ifstream tf("test4.exe",std::ios::binary);
  std::string str2((std::istreambuf_iterator<char>(tf)),std::istreambuf_iterator<char>());
  std::string half2 = str2.substr(0, str2.length()/2);
  std::string otherHlf = str2.substr(str2.length()/2);
  string jj = decrypt(half2,ky);
  string jj2 = decrypt(otherHlf,ky);
  sleep(1);
  std::ofstream myfile4("test5.exe",std::ios::binary);
  if(myfile4.is_open())
    {
      myfile4 << jj+jj2 << std::endl;
    }    
}