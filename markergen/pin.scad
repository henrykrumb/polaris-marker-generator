$fn = 40;

module pin() {
  h1 = 0.46;
  h2 = 2.3;
  h3 = 0.975;
  h4 = 0.6;
  h5 = 0.81;
  h6 = 2.1;

  difference() {

    union() {
      cylinder(h1, r=5.59 / 2);
      translate([0, 0, h1]) {
        cylinder(h2, r1=5.59 / 2, r2=3.3 / 2);
        translate([0, 0, h2]) {
          cylinder(h3, r=3.5 / 2);
          translate([0, 0, h3]) {
            cylinder(h4, r=2.2 / 2);
            translate([0, 0, h4]) {
              cylinder(h5, r1=2.2 / 2, r2=3 / 2);
              translate([0, 0, h5]) {
                cylinder(h6, r1=3 / 2, r2=1.7 / 2);
              }
            }
          }
        }
      }
    }
  
    translate([0, 0, h1 + h2 + h3 + h4 + h5 + 1e-3])
    cylinder(r=0.7 / 2, h=h6);
    
  }
}
