// Imports
#import "@preview/brilliant-cv:2.0.3": letter
#let metadata = toml("./metadata.toml")


#show: letter.with(
  metadata,
  myAddress: "Your Address Here",
  recipientName: "Landsea Homes",
  recipientAddress: "Company Address Here",
  date: datetime.today().display(),
  subject: "Subject: Application for [Position Title]",
  signature: image("src/signature.png"),
)

Dear Hiring Manager,

I’m a Seattle-based Construction Manager with 20+ years delivering multifamily, high-rise, senior living, and luxury residential projects. My background includes high-end custom homes with Toth Construction and ultra-luxury resort residential work with Discovery Land Company, along with large technical builds across Seattle, LA, and Chicago.

I lead with strong field presence, clear communication, and disciplined scheduling. I’m fluent in the Seattle subcontractor network, permitting processes, and managing multiple jobsites while maintaining quality, safety, and cost control. My teams rely on predictable planning, early problem-solving, and coordination that keeps owners confident and projects on track.

Landsea’s focus on autonomy, accountability, and high standards aligns with how I run work. I’d bring deep regional experience, luxury-level quality expectations, and steady leadership to support your projects in Issaquah and the surrounding area.

I’d welcome a conversation about how I can contribute.

—Michael Colenso

