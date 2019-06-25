using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace Generate_points
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        string folder;
        List<string> image_str = new List<string>();

        List<Rectangle> rects = new List<Rectangle>();

        Point firstPoint = new Point();
        Point secondPoint = new Point();



        private void button1_Click(object sender, EventArgs e)
        {
            if(folderBrowserDialog1.ShowDialog() == DialogResult.OK)
            {
                folder = folderBrowserDialog1.SelectedPath;
            }

            image_str = Directory.GetFiles(folder, ".", SearchOption.AllDirectories).ToList();

            pictureBox1.BackgroundImage = new Bitmap(image_str[0]);

        }

        private void pictureBox1_MouseClick(object sender, MouseEventArgs e)
        {

            

        }
    }
}
