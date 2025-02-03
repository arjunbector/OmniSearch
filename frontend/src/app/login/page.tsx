import GoogleLogin from "@/components/ui/google-login";
import MaxWidthWrapper from "@/components/ui/max-width-wrapper";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Login",
};

const LoginPage = () => {
  return (
    <MaxWidthWrapper>
      <GoogleLogin />
    </MaxWidthWrapper>
  );
};

export default LoginPage;
